"""CICDDoS2019 leakage audit and shortcut-feature ablations.

Training-only imputation. Exact-duplicate and group-overlap audit.
Staged ablations removing Timestamp, Inbound, and port features.
Does not invent scores.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix, matthews_corrcoef
from sklearn.model_selection import train_test_split


def _find_col(columns, name: str) -> str | None:
    target = name.strip().lower()
    for col in columns:
        if str(col).strip().lower() == target:
            return col
    return None


def rates(y_true, y_pred) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        "far": float(fp / (fp + tn)) if (fp + tn) else None,
        "fnr": float(fn / (fn + tp)) if (fn + tp) else None,
        "mcc": float(matthews_corrcoef(y_true, y_pred)) if len(np.unique(y_true)) > 1 else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True, help="all-data.csv")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-rows", type=int, default=200_000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    head = args.data.read_bytes()[:40]
    if head.lstrip().startswith(b"<") or b"html" in head[:20].lower():
        raise SystemExit("Refused HTML masquerading as CSV")

    df = pd.read_csv(args.data, nrows=args.max_rows, low_memory=False)
    label_col = _find_col(df.columns, "Label")
    if label_col is None:
        raise SystemExit(f"No Label column; got {list(df.columns)[:15]}")
    y = (df[label_col].astype(str).str.strip().str.upper() != "BENIGN").astype(np.int8).to_numpy()

    src_ip = _find_col(df.columns, "Source IP")
    dst_ip = _find_col(df.columns, "Destination IP")
    flow_id = _find_col(df.columns, "Flow ID")
    ts_col = _find_col(df.columns, "Timestamp")
    inbound = _find_col(df.columns, "Inbound")
    sport = _find_col(df.columns, "Source Port")
    dport = _find_col(df.columns, "Destination Port")

    # Exact duplicate audit on all columns except any index leftovers.
    dup_mask = df.duplicated(keep=False)
    exact_dups = int(dup_mask.sum())

    group_keys = [c for c in [src_ip, dst_ip, sport, dport, flow_id] if c]
    overlap_report = {"exact_duplicate_rows": exact_dups, "group_keys": group_keys}

    # Feature sets
    drop_always = {label_col, src_ip, dst_ip, flow_id, _find_col(df.columns, "SimillarHTTP"), _find_col(df.columns, "Unnamed: 0")}
    drop_always = {c for c in drop_always if c}
    numeric_cols = [c for c in df.columns if c not in drop_always and pd.api.types.is_numeric_dtype(df[c])]

    # Optional timestamp unix conversion if present as datetime-like object column.
    feature_frames = {}
    base = df[numeric_cols].replace([np.inf, -np.inf], np.nan)
    feature_frames["full_numeric"] = base
    drop_ts = [c for c in numeric_cols if c != ts_col and "timestamp" not in str(c).strip().lower()]
    feature_frames["no_timestamp"] = df[drop_ts].replace([np.inf, -np.inf], np.nan) if drop_ts else base
    drop_inbound = [c for c in drop_ts if c != inbound]
    feature_frames["no_timestamp_inbound"] = df[drop_inbound].replace([np.inf, -np.inf], np.nan)
    drop_ports = [c for c in drop_inbound if c not in {sport, dport}]
    feature_frames["no_timestamp_inbound_ports"] = df[drop_ports].replace([np.inf, -np.inf], np.nan)

    idx = np.arange(len(df))
    train_idx, temp_idx = train_test_split(idx, test_size=0.30, random_state=args.seed, stratify=y)
    val_idx, test_idx = train_test_split(temp_idx, test_size=0.50, random_state=args.seed, stratify=y[temp_idx])

    # Group leakage: shared flow identifiers across splits
    if flow_id:
        train_flows = set(df.iloc[train_idx][flow_id].astype(str))
        test_flows = set(df.iloc[test_idx][flow_id].astype(str))
        overlap_report["flow_id_train_test_overlap"] = int(len(train_flows & test_flows))
        overlap_report["flow_id_train"] = int(len(train_flows))
        overlap_report["flow_id_test"] = int(len(test_flows))
    if src_ip and dst_ip:
        def pairset(indices):
            return set(zip(df.iloc[indices][src_ip].astype(str), df.iloc[indices][dst_ip].astype(str)))
        overlap_report["src_dst_pair_train_test_overlap"] = int(len(pairset(train_idx) & pairset(test_idx)))

    results = {"seed": args.seed, "rows": int(len(df)), "overlap": overlap_report, "configs": {}}
    score_rows = []
    for name, frame in feature_frames.items():
        imputer = SimpleImputer(strategy="median")
        x_train = imputer.fit_transform(frame.iloc[train_idx])
        x_val = imputer.transform(frame.iloc[val_idx])
        x_test = imputer.transform(frame.iloc[test_idx])
        # Contaminated baseline: impute on all rows then split (for comparison only)
        imputer_all = SimpleImputer(strategy="median")
        x_all = imputer_all.fit_transform(frame)
        model = RandomForestClassifier(
            n_estimators=80, max_depth=24, min_samples_leaf=5,
            class_weight="balanced_subsample", n_jobs=-1, random_state=args.seed,
        )
        model.fit(x_train, y[train_idx])
        val_scores = model.predict_proba(x_val)[:, 1]
        test_scores = model.predict_proba(x_test)[:, 1]
        pred = (test_scores >= 0.5).astype(int)
        cfg = {
            "n_features": int(frame.shape[1]),
            "features": list(frame.columns[:80]),
            "test_threshold_0.5": rates(y[test_idx], pred),
            "imputation": "training_only_median",
        }
        # Contaminated comparator
        model_c = RandomForestClassifier(
            n_estimators=80, max_depth=24, min_samples_leaf=5,
            class_weight="balanced_subsample", n_jobs=-1, random_state=args.seed,
        )
        model_c.fit(x_all[train_idx], y[train_idx])
        pred_c = (model_c.predict_proba(x_all[test_idx])[:, 1] >= 0.5).astype(int)
        cfg["contaminated_pre_split_imputation_test_threshold_0.5"] = rates(y[test_idx], pred_c)
        results["configs"][name] = cfg
        for split, scores, labels, indices in (
            ("val", val_scores, y[val_idx], val_idx),
            ("test", test_scores, y[test_idx], test_idx),
        ):
            for i, score, lab in zip(indices, scores, labels):
                score_rows.append({
                    "target_id": f"{split}_{int(i)}",
                    "y_true": int(lab),
                    "score_attack": float(score),
                    "model": f"RF_{name}",
                    "seed": args.seed,
                    "split": split,
                })
        print(name, cfg["test_threshold_0.5"], flush=True)

    pd.DataFrame(score_rows).to_csv(args.out / "predictions.csv", index=False)
    (args.out / "leakage_shortcut_report.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "out": str(args.out), "configs": list(results["configs"])}))


if __name__ == "__main__":
    main()
