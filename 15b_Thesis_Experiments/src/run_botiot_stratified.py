"""BoT-IoT rerun that keeps every benign row, then fills with attack rows.

Uses the Zenodo audit trainer on a stratified extract from complete Full5pc CSVs.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "zenodo uploads" / "code" / "run_botiot_audit.py"
sys.path.insert(0, str(AUDIT.parent))

spec = importlib.util.spec_from_file_location("run_botiot_audit", AUDIT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def stratified_frame(data_dir: Path, max_rows: int, seed: int) -> pd.DataFrame:
    columns = sorted(set(audit.FLOW + audit.PORTS + audit.AGGREGATES + audit.LABELS))
    paths = sorted(data_dir.glob("UNSW_2018_IoT_Botnet_Full5pc_*.csv"))
    if len(paths) != 4:
        raise SystemExit(f"Need 4 CSVs, found {[p.name for p in paths]}")
    # Load all benign first (rare), then fill remaining budget with attacks.
    benign_parts, attack_parts = [], []
    for path in paths:
        print(f"scanning {path.name}", flush=True)
        for chunk in pd.read_csv(audit.complete_csv(path), usecols=columns, chunksize=200_000, low_memory=False):
            for col in columns:
                if col == "category":
                    continue
                chunk[col] = pd.to_numeric(chunk[col], errors="coerce").astype(np.float32)
            chunk["category"] = chunk["category"].astype(str)
            attack = chunk["attack"].fillna(0).astype(np.int8)
            benign_parts.append(chunk.loc[attack == 0])
            attack_parts.append(chunk.loc[attack == 1])
    benign = pd.concat(benign_parts, ignore_index=True) if benign_parts else pd.DataFrame(columns=columns)
    attack = pd.concat(attack_parts, ignore_index=True) if attack_parts else pd.DataFrame(columns=columns)
    print(f"benign_total={len(benign)} attack_total={len(attack)}", flush=True)
    remain = max(max_rows - len(benign), 0)
    rng = np.random.default_rng(seed)
    if remain and len(attack):
        take = min(remain, len(attack))
        chosen = rng.choice(len(attack), size=take, replace=False)
        attack = attack.iloc[chosen]
    else:
        attack = attack.iloc[0:0]
    frame = pd.concat([benign, attack], ignore_index=True)
    frame = frame.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    print(f"stratified_rows={len(frame)} attack_rate={frame['attack'].mean():.6f}", flush=True)
    return frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-rows", type=int, default=400_000)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 7, 123])
    args = parser.parse_args()
    frame = stratified_frame(args.data, args.max_rows, seed=42)
    report = {
        "source": "UNSW Canberra BoT-IoT 5% extract, stratified benign-preserving subsample",
        "provenance": "kaggle_mirror_bot-iot-5-data",
        "files": [p.name for p in sorted(args.data.glob('UNSW_2018_IoT_Botnet_Full5pc_*.csv'))],
        "file_shortfalls": [],
        "rows": int(len(frame)),
        "max_rows": args.max_rows,
        "attack_rate": float(frame["attack"].mean()),
        "categories": {str(k): int(v) for k, v in frame["category"].value_counts().items()},
        "dropped_identifiers": ["pkSeqID", "stime", "ltime", "seq", "saddr", "daddr"],
        "note": (
            "Every benign/Normal row from the four complete CSVs is retained; "
            "attack rows are subsampled to the max-rows budget. "
            "False-alarm claims remain limited by benign support."
        ),
        "populations": {},
    }
    for population in ("all", "ddos_dos_normal"):
        mask = audit.population_mask(frame["category"].to_numpy(), population)
        subset = frame.loc[mask].reset_index(drop=True)
        print(f"population {population} rows {len(subset)}", flush=True)
        report["populations"][population] = {"rows": int(len(subset)), "configs": {}}
        for config, features in audit.CONFIGS.items():
            if population == "ddos_dos_normal" and config != "audited_flow":
                continue
            seeds = args.seeds if config == "audited_flow" else [args.seeds[0]]
            if population == "ddos_dos_normal":
                seeds = [args.seeds[0]]
            config_out = {"features": features, "seeds": {}}
            for seed in seeds:
                scaled, y, _category, train_idx, val_idx, test_idx = audit.prepare(subset, features, seed)
                print(
                    f"  seed {seed} train {len(train_idx)} val {len(val_idx)} test {len(test_idx)} "
                    f"benign {int((y[train_idx]==0).sum())}/{int((y[val_idx]==0).sum())}/{int((y[test_idx]==0).sum())}",
                    flush=True,
                )
                models = audit.fit_models(seed, scaled[train_idx], y[train_idx])
                seed_out = {"models": {}}
                for name, model in models.items():
                    scored = audit.score_model(model, scaled[val_idx], y[val_idx], scaled[test_idx], y[test_idx])
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
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(__import__("json").dumps(report, indent=2), encoding="utf-8")
    args.out.write_text(__import__("json").dumps(report, indent=2), encoding="utf-8")
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
