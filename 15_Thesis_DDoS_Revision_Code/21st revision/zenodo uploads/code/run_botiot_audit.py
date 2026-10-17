#!/usr/bin/env python3
"""Leakage-aware BoT-IoT 5% replication.

Independent within-dataset comparison. Not a transfer from CICIoT2023.
Addresses, timestamps, row indexes, and IP-grouped aggregate fields are
removed in the audited configuration. Medians and the min-max scaler are
fit on training rows only. Every model is scored on the same validation
and test records. False-alarm thresholds are chosen on validation.
"""
from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, matthews_corrcoef, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier

FLOW = [
    "flgs_number", "proto_number", "pkts", "bytes", "state_number",
    "dur", "mean", "stddev", "sum", "min", "max",
    "spkts", "dpkts", "sbytes", "dbytes", "rate", "srate", "drate",
]
PORTS = ["sport", "dport"]
AGGREGATES = [
    "TnBPSrcIP", "TnBPDstIP", "TnP_PSrcIP", "TnP_PDstIP", "TnP_PerProto", "TnP_Per_Dport",
    "AR_P_Proto_P_SrcIP", "AR_P_Proto_P_DstIP", "N_IN_Conn_P_DstIP", "N_IN_Conn_P_SrcIP",
    "AR_P_Proto_P_Sport", "AR_P_Proto_P_Dport",
    "Pkts_P_State_P_Protocol_P_DestIP", "Pkts_P_State_P_Protocol_P_SrcIP",
]
LABELS = ["attack", "category"]
CONFIGS = {
    "audited_flow": FLOW,
    "audited_plus_ports": FLOW + PORTS,
    "flow_plus_ip_aggregates": FLOW + AGGREGATES,
}
BUDGETS = (("far_0.1pct", 0.001), ("far_0.02pct", 0.0002))


def complete_csv(path: Path) -> io.BytesIO:
    """Drop a trailing partial record left by a download that stopped at 256 MiB."""
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        cut = raw.rfind(b"\n")
        raw = raw[: cut + 1] if cut >= 0 else b""
    return io.BytesIO(raw)


def read_frame(paths: list[Path], columns: list[str], max_rows: int | None) -> pd.DataFrame:
    frames = []
    kept = 0
    for path in paths:
        for chunk in pd.read_csv(complete_csv(path), usecols=columns, chunksize=150_000, low_memory=False):
            if max_rows is not None:
                chunk = chunk.iloc[: max(0, max_rows - kept)]
            frames.append(chunk)
            kept += len(chunk)
            if max_rows is not None and kept >= max_rows:
                break
        if max_rows is not None and kept >= max_rows:
            break
    frame = pd.concat(frames, ignore_index=True)
    for column in columns:
        if column == "category":
            continue
        frame[column] = pd.to_numeric(frame[column], errors="coerce").astype(np.float32)
    frame["category"] = frame["category"].astype(str)
    return frame


def rates(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    benign = int(tn + fp)
    attack = int(fn + tp)
    far = float(fp / benign) if benign else float("nan")
    fnr = float(fn / attack) if attack else float("nan")
    mcc = float(matthews_corrcoef(y_true, y_pred)) if len(np.unique(y_true)) > 1 else float("nan")
    return {
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        "benign": benign, "attack": attack,
        "far": far, "fnr": fnr, "mcc": mcc,
    }


def threshold_for_budget(y_true: np.ndarray, scores: np.ndarray, budget: float) -> float:
    benign_scores = scores[y_true == 0]
    if len(benign_scores) == 0:
        return 1.0
    allowed = int(np.floor(budget * len(benign_scores)))
    order = np.argsort(benign_scores)[::-1]
    if allowed <= 0:
        return float(benign_scores.max()) + 1e-6
    if allowed >= len(benign_scores):
        return float(benign_scores.min())
    boundary = float(benign_scores[order[allowed]])
    return float(np.nextafter(np.float64(boundary), np.float64(np.inf)))


def fit_models(seed: int, x_train: np.ndarray, y_train: np.ndarray):
    models = {
        "Decision Tree": DecisionTreeClassifier(
            class_weight="balanced", max_depth=24, min_samples_leaf=20, random_state=seed
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=80, max_depth=24, min_samples_leaf=5,
            class_weight="balanced_subsample", max_samples=min(150_000, len(y_train)),
            n_jobs=2, random_state=seed,
        ),
        "HistGradientBoosting": HistGradientBoostingClassifier(
            max_iter=120, learning_rate=0.08, class_weight="balanced", random_state=seed
        ),
        "Logistic Regression": LogisticRegression(
            class_weight="balanced", max_iter=300, solver="lbfgs"
        ),
    }
    if len(y_train) > 180_000 and len(np.unique(y_train)) > 1:
        rng = np.random.default_rng(seed)
        benign = np.flatnonzero(y_train == 0)
        attack = np.flatnonzero(y_train == 1)
        take_b = min(len(benign), 40_000)
        take_a = min(len(attack), 140_000)
        chosen = np.concatenate([
            rng.choice(benign, size=take_b, replace=False) if take_b else np.array([], dtype=int),
            rng.choice(attack, size=take_a, replace=False) if take_a else np.array([], dtype=int),
        ])
        lr_x, lr_y = x_train[chosen], y_train[chosen]
    else:
        lr_x, lr_y = x_train, y_train
    if len(np.unique(y_train)) < 2:
        raise ValueError("training labels contain one class")
    fitted = {}
    for name, model in models.items():
        if name == "Logistic Regression":
            model.fit(lr_x, lr_y)
        else:
            model.fit(x_train, y_train)
        fitted[name] = model
        print(f"    fitted {name}", flush=True)
    return fitted


def score_model(model, x_val, y_val, x_test, y_test) -> dict:
    val_scores = model.predict_proba(x_val)[:, 1]
    test_scores = model.predict_proba(x_test)[:, 1]
    out = {"roc_auc": float(roc_auc_score(y_test, test_scores))}
    n_benign_val = int((y_val == 0).sum())
    one_fp_budget = (1 / n_benign_val) if n_benign_val else 1.0
    cuts = [("threshold_0.5", 0.5), ("at_most_one_validation_fp", threshold_for_budget(y_val, val_scores, one_fp_budget))]
    for name, budget in BUDGETS:
        cuts.append((name, threshold_for_budget(y_val, val_scores, budget)))
    for name, threshold in cuts:
        pred = (test_scores >= threshold).astype(np.int8)
        row = rates(y_test, pred)
        row["threshold"] = float(threshold)
        val_pred = (val_scores >= threshold).astype(np.int8)
        val_rates = rates(y_val, val_pred)
        row["validation_far"] = val_rates["far"]
        row["validation_fp"] = val_rates["fp"]
        row["validation_benign"] = val_rates["benign"]
        out[name] = row
    if hasattr(model, "feature_importances_"):
        out["importances"] = [float(v) for v in model.feature_importances_]
    return out


def prepare(frame: pd.DataFrame, columns: list[str], seed: int):
    work = frame[columns + ["attack", "category"]].replace([np.inf, -np.inf], np.nan)
    y = work["attack"].fillna(0).astype(np.int8).to_numpy()
    category = work["category"].to_numpy()
    index = np.arange(len(work))
    train_idx, temp_idx = train_test_split(index, test_size=0.30, random_state=seed, stratify=y)
    val_idx, test_idx = train_test_split(temp_idx, test_size=0.50, random_state=seed, stratify=y[temp_idx])
    medians = work.iloc[train_idx][columns].median(numeric_only=True)
    filled = work[columns].fillna(medians).astype(np.float32)
    scaler = MinMaxScaler()
    scaler.fit(filled.iloc[train_idx])
    scaled = scaler.transform(filled).astype(np.float32)
    return scaled, y, category, train_idx, val_idx, test_idx


def population_mask(category: np.ndarray, population: str) -> np.ndarray:
    if population == "all":
        return np.ones(len(category), dtype=bool)
    keep = {"Normal", "DDoS", "DoS"}
    return np.array([value in keep for value in category], dtype=bool)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 7, 123])
    args = parser.parse_args()
    expected = {
        "UNSW_2018_IoT_Botnet_Full5pc_1.csv": 272335105,
        "UNSW_2018_IoT_Botnet_Full5pc_2.csv": 273082424,
        "UNSW_2018_IoT_Botnet_Full5pc_3.csv": 282131555,
        "UNSW_2018_IoT_Botnet_Full5pc_4.csv": 189577740,
    }
    # Verified complete Kaggle mirror (vigneshvenkateswaran/bot-iot-5-data). Same
    # 5% all-features schema; byte sizes differ from CloudStor published lengths.
    kaggle_mirror = {
        "UNSW_2018_IoT_Botnet_Full5pc_1.csv": 277_543_651,
        "UNSW_2018_IoT_Botnet_Full5pc_2.csv": 278_451_723,
        "UNSW_2018_IoT_Botnet_Full5pc_3.csv": 285_316_035,
        "UNSW_2018_IoT_Botnet_Full5pc_4.csv": 191_754_639,
    }
    accepted_short = {"UNSW_2018_IoT_Botnet_Full5pc_3.csv": 268_435_456}
    paths = []
    shortfalls = []
    provenance = "official_or_unknown"
    for path in sorted(args.data.glob("UNSW_2018_IoT_Botnet_Full5pc_*.csv")):
        size = path.stat().st_size
        official = expected.get(path.name)
        if size == official or size == accepted_short.get(path.name) or size == kaggle_mirror.get(path.name):
            # Refuse the known truncated 256 MiB file 3.
            if size == accepted_short.get(path.name):
                shortfalls.append({
                    "file": path.name,
                    "official_bytes": official,
                    "local_bytes": size,
                    "missing_bytes": (official - size) if official else None,
                    "handling": "TRUNCATED_REFUSED",
                })
                continue
            paths.append(path)
            if size == kaggle_mirror.get(path.name):
                provenance = "kaggle_mirror_bot-iot-5-data"
            if official is not None and size != official:
                shortfalls.append({
                    "file": path.name,
                    "official_bytes": official,
                    "local_bytes": size,
                    "missing_bytes": official - size,
                    "handling": "complete alternate mirror; not the truncated 256 MiB copy",
                })
    if args.max_rows is None and len(paths) != 4:
        raise SystemExit(f"Need all 4 BoT-IoT files, found {[path.name for path in paths]}")
    if not paths:
        raise SystemExit(f"No complete BoT-IoT CSVs in {args.data}")
    columns = sorted(set(FLOW + PORTS + AGGREGATES + LABELS))
    print(f"reading {len(paths)} files", flush=True)
    frame = read_frame(paths, columns, args.max_rows)
    print(f"rows {len(frame)} attack rate {frame['attack'].mean():.6f}", flush=True)
    print(frame["category"].value_counts().to_dict(), flush=True)
    report = {
        "source": "UNSW Canberra official BoT-IoT 5% extract, All features, Full5pc CSV files",
        "files": [path.name for path in paths],
        "file_shortfalls": shortfalls,
        "rows": int(len(frame)),
        "max_rows": args.max_rows,
        "attack_rate": float(frame["attack"].mean()),
        "categories": {str(k): int(v) for k, v in frame["category"].value_counts().items()},
        "dropped_identifiers": ["pkSeqID", "stime", "ltime", "seq", "saddr", "daddr"],
        "note": (
            "Independent replication on BoT-IoT records. Not a cross-dataset transfer. "
            "Training subsamples apply only to random-forest tree bags (max_samples=150000) "
            "and, above 180000 training rows, to logistic regression. "
            "HistGradientBoosting and the decision tree use every training row. "
            "Validation and test scores use every selected record."
        ),
        "populations": {},
    }
    for population in ("all", "ddos_dos_normal"):
        mask = population_mask(frame["category"].to_numpy(), population)
        subset = frame.loc[mask].reset_index(drop=True)
        print(f"population {population} rows {len(subset)}", flush=True)
        report["populations"][population] = {"rows": int(len(subset)), "configs": {}}
        for config, features in CONFIGS.items():
            if population == "ddos_dos_normal" and config != "audited_flow":
                continue
            seeds = args.seeds if config == "audited_flow" else [args.seeds[0]]
            if population == "ddos_dos_normal":
                seeds = [args.seeds[0]]
            print(f"  config {config} seeds {seeds}", flush=True)
            config_out = {"features": features, "seeds": {}}
            for seed in seeds:
                scaled, y, _category, train_idx, val_idx, test_idx = prepare(subset, features, seed)
                print(
                    f"  seed {seed} train {len(train_idx)} val {len(val_idx)} test {len(test_idx)} "
                    f"benign {int((y[train_idx]==0).sum())}/{int((y[val_idx]==0).sum())}/{int((y[test_idx]==0).sum())}",
                    flush=True,
                )
                models = fit_models(seed, scaled[train_idx], y[train_idx])
                seed_out = {"models": {}}
                for name, model in models.items():
                    scored = score_model(model, scaled[val_idx], y[val_idx], scaled[test_idx], y[test_idx])
                    if "importances" in scored and name == "Decision Tree":
                        scored["importance_pairs"] = sorted(
                            zip(features, scored["importances"]), key=lambda item: item[1], reverse=True
                        )
                        scored["importance_pairs"] = [
                            [feature, round(value, 6)] for feature, value in scored["importance_pairs"][:8]
                        ]
                    seed_out["models"][name] = scored
                    point = scored["threshold_0.5"]
                    print(
                        f"    {name} FP {point['fp']} FN {point['fn']} FAR {point['far']:.6f} FNR {point['fnr']:.6f}",
                        flush=True,
                    )
                config_out["seeds"][str(seed)] = seed_out
            report["populations"][population]["configs"][config] = config_out
            args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
