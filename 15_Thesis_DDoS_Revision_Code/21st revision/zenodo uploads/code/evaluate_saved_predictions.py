"""Matched false-alarm evaluation from saved scores.

Expected file: a CSV with columns
    model, split, y_true, y_score
Optional column:
    seed

split must contain 'val' (or 'validation') and 'test'.
y_true is 1 for attack and 0 for benign.
y_score is the predicted attack probability.

Thresholds are chosen on validation rows only. Test rows are scored after
the threshold has been fixed. If the file is absent, this script writes a
status note and does not invent metrics.

Example:
    python evaluate_saved_predictions.py --predictions predictions/scores.csv --out output/matched_far.csv
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

TARGETS = (0.0001, 0.0005, 0.001, 0.005, 0.01)  # false-alarm proportions: 0.01% ... 1%


def _split_name(value: str) -> str:
    text = value.strip().lower()
    if text in {"val", "valid", "validation"}:
        return "val"
    if text == "test":
        return "test"
    return text


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        required = {"model", "split", "y_true", "y_score"}
        missing = required - fields
        if missing:
            raise SystemExit(f"Missing columns: {sorted(missing)}")
        rows = []
        for raw in reader:
            rows.append({
                "model": raw["model"],
                "seed": raw.get("seed", "1"),
                "split": _split_name(raw["split"]),
                "y_true": int(raw["y_true"]),
                "y_score": float(raw["y_score"]),
            })
    return rows


def _rates(y_true: np.ndarray, y_score: np.ndarray, threshold: float) -> dict:
    pred = y_score >= threshold
    attack = y_true == 1
    benign = ~attack
    tp = int(np.sum(pred & attack))
    fn = int(np.sum(~pred & attack))
    fp = int(np.sum(pred & benign))
    tn = int(np.sum(~pred & benign))
    far = fp / (fp + tn) if (fp + tn) else float("nan")
    fnr = fn / (fn + tp) if (fn + tp) else float("nan")
    tpr = tp / (tp + fn) if (tp + fn) else float("nan")
    return {"TP": tp, "FP": fp, "TN": tn, "FN": fn, "FAR": far, "FNR": fnr, "TPR": tpr}


def choose_threshold(y_true: np.ndarray, y_score: np.ndarray, target_far: float) -> tuple[float | None, float]:
    """Highest validation true-positive rate among thresholds with FAR <= target.

    Returns (threshold, validation FAR). threshold is None when the target is
    not achievable on the validation benign rows.
    """
    benign = y_score[y_true == 0]
    if benign.size == 0:
        return None, float("nan")
    # A threshold above every benign score yields FAR = 0 if any such value exists.
    candidates = np.unique(np.concatenate([y_score, np.array([1.0 + 1e-12])]))
    best_t = None
    best_tpr = -1.0
    best_far = float("nan")
    for threshold in candidates:
        stats = _rates(y_true, y_score, float(threshold))
        if np.isnan(stats["FAR"]) or stats["FAR"] > target_far + 1e-15:
            continue
        if stats["TPR"] > best_tpr:
            best_tpr = stats["TPR"]
            best_t = float(threshold)
            best_far = stats["FAR"]
    return best_t, best_far


def evaluate(rows: list[dict], targets=TARGETS) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        grouped.setdefault((row["model"], row["seed"]), []).append(row)
    results = []
    for (model, seed), group in sorted(grouped.items()):
        val = [r for r in group if r["split"] == "val"]
        test = [r for r in group if r["split"] == "test"]
        if not val or not test:
            raise SystemExit(f"{model} seed {seed} needs both validation and test rows.")
        yv = np.array([r["y_true"] for r in val])
        sv = np.array([r["y_score"] for r in val])
        yt = np.array([r["y_true"] for r in test])
        st = np.array([r["y_score"] for r in test])
        for target in targets:
            threshold, val_far = choose_threshold(yv, sv, target)
            if threshold is None:
                results.append({
                    "model": model,
                    "seed": seed,
                    "target_FAR": target,
                    "status": "not achievable on validation",
                    "threshold": "",
                    "validation_FAR": "",
                    "test_FAR": "",
                    "test_FNR": "",
                    "test_TPR": "",
                    "test_TP": "",
                    "test_FP": "",
                    "test_TN": "",
                    "test_FN": "",
                })
                continue
            stats = _rates(yt, st, threshold)
            results.append({
                "model": model,
                "seed": seed,
                "target_FAR": target,
                "status": "ok",
                "threshold": f"{threshold:.6f}",
                "validation_FAR": f"{val_far:.6g}",
                "test_FAR": f"{stats['FAR']:.6g}",
                "test_FNR": f"{stats['FNR']:.6g}",
                "test_TPR": f"{stats['TPR']:.6g}",
                "test_TP": stats["TP"],
                "test_FP": stats["FP"],
                "test_TN": stats["TN"],
                "test_FN": stats["FN"],
            })
    return results


def write_status(path: Path, message: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(message + "\n", encoding="utf-8")


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Matched-FAR evaluation from saved scores.")
    parser.add_argument("--predictions", type=Path, default=here.parent / "predictions" / "scores.csv")
    parser.add_argument("--out", type=Path, default=here / "output" / "matched_far.csv")
    args = parser.parse_args()
    if not args.predictions.exists():
        message = (
            "No prediction file was found at "
            f"{args.predictions}. Matched false-alarm results were not computed. "
            "Place a CSV with columns model, split, y_true, y_score (and optional seed) "
            "and run this script again. This file must not be cited as an experimental result."
        )
        write_status(args.out.with_name("MATCHED_FAR_NOT_RUN.txt"), message)
        print(message)
        return
    rows = load_rows(args.predictions)
    results = evaluate(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"Wrote {len(results)} rows to {args.out}")


if __name__ == "__main__":
    main()
