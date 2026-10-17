"""Build all-data.csv from CICDDoS2019 day-01-12 CSVs using the thesis downsample rule.

mult=5 attack:benign within each file; random_state=42. Does not invent labels.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.utils import resample

MULT = 5
SEED = 42


def _label_col(columns) -> str:
    for name in columns:
        if name.strip().lower() == "label":
            return name
    raise ValueError(f"No Label column in {list(columns)[:10]}")


def load_file(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    label = None
    ok_parts, ddos_parts = [], []
    for chunk in pd.read_csv(path, chunksize=400_000, low_memory=False):
        if label is None:
            label = _label_col(chunk.columns)
        is_benign = chunk[label].astype(str).str.strip().str.upper() == "BENIGN"
        flows_ok = chunk[is_benign]
        flows_ddos = chunk[~is_benign]
        if len(flows_ok) * MULT < len(flows_ddos):
            flows_ddos = resample(
                flows_ddos, replace=False, n_samples=len(flows_ok) * MULT, random_state=SEED
            )
        ok_parts.append(flows_ok)
        ddos_parts.append(flows_ddos)
    return pd.concat(ok_parts, ignore_index=True), pd.concat(ddos_parts, ignore_index=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-files", type=int, default=None)
    args = parser.parse_args()
    files = sorted(args.raw.glob("*.csv"))
    if args.max_files:
        files = files[: args.max_files]
    if not files:
        raise SystemExit(f"No CSVs in {args.raw}")
    ok_all, ddos_all = [], []
    for path in files:
        print(f"loading {path.name} ({path.stat().st_size} bytes)", flush=True)
        ok, ddos = load_file(path)
        print(f"  benign={len(ok)} attack={len(ddos)}", flush=True)
        ok_all.append(ok)
        ddos_all.append(ddos)
    merged = pd.concat(ok_all + ddos_all, ignore_index=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(args.out, index=False)
    # Reject HTML
    head = args.out.read_bytes()[:20]
    if head.lstrip().startswith(b"<"):
        raise SystemExit("Refused: output looks like HTML")
    print(f"wrote {args.out} rows={len(merged)} bytes={args.out.stat().st_size}", flush=True)


if __name__ == "__main__":
    main()
