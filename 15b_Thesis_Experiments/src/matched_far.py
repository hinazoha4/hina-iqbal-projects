"""Select a false-alarm threshold on validation scores and score the same targets on test.

This module does not create scores. Both files need target_id, y_true, score_attack, model, and seed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def validate(frame: pd.DataFrame) -> None:
    needed = {"target_id", "y_true", "score_attack", "model", "seed"}
    missing = needed - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if frame[list(needed)].isna().any().any():
        raise ValueError("Null in required columns")
    if not set(frame["y_true"].unique()).issubset({0, 1}):
        raise ValueError("y_true must be binary: 0 benign, 1 attack")
    scores = frame["score_attack"]
    if ((scores < 0) | (scores > 1)).any():
        raise ValueError("Scores outside [0, 1]")
    if frame.duplicated(["model", "seed", "target_id"]).any():
        raise ValueError("Duplicate predictions for a target, model, and seed")


def threshold_for_budget(val: pd.DataFrame, budget: float) -> tuple[float, int]:
    scores = val["score_attack"].to_numpy(dtype=float)
    labels = val["y_true"].to_numpy()
    benign = scores[labels == 0]
    if len(benign) == 0:
        raise ValueError("No benign validation observations")
    candidates = np.r_[np.unique(scores), np.nextafter(np.max(scores), np.inf)]
    ordered = np.sort(benign)
    false_positives = len(ordered) - np.searchsorted(ordered, candidates, side="left")
    eligible = candidates[false_positives / len(ordered) <= budget + 1e-12]
    if len(eligible) == 0:
        raise ValueError("No threshold meets the validation false-alarm budget")
    return float(eligible[0]), len(ordered)


def score(test: pd.DataFrame, threshold: float) -> dict:
    predicted = test["score_attack"].to_numpy() >= threshold
    labels = test["y_true"].to_numpy()
    tp = int(((predicted == 1) & (labels == 1)).sum())
    tn = int(((predicted == 0) & (labels == 0)).sum())
    fp = int(((predicted == 1) & (labels == 0)).sum())
    fn = int(((predicted == 0) & (labels == 1)).sum())
    return {
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "far": fp / (fp + tn) if (fp + tn) else None,
        "fnr": fn / (fn + tp) if (fn + tp) else None,
    }


def evaluate(validation: pd.DataFrame, test: pd.DataFrame, budgets: list[float]) -> pd.DataFrame:
    validate(validation)
    validate(test)
    if set(validation["target_id"].astype(str)) & set(test["target_id"].astype(str)):
        raise ValueError("Target IDs overlap validation and test")
    rows = []
    for seed in sorted(test["seed"].unique()):
        validation_seed = validation[validation["seed"] == seed]
        test_seed = test[test["seed"] == seed]
        reference = None
        for model in sorted(test_seed["model"].unique()):
            subset = test_seed[test_seed["model"] == model].set_index("target_id").sort_index()
            if reference is None:
                reference = subset["y_true"]
            elif not subset["y_true"].index.equals(reference.index) or not subset["y_true"].equals(reference):
                raise ValueError(f"Unpaired test targets for seed={seed} model={model}")
        for model in sorted(test_seed["model"].unique()):
            model_validation = validation_seed[validation_seed["model"] == model]
            model_test = test_seed[test_seed["model"] == model]
            for budget in budgets:
                threshold, n_benign = threshold_for_budget(model_validation, budget)
                rows.append({
                    "seed": seed,
                    "model": model,
                    "validation_benign": n_benign,
                    "target_far": budget,
                    "threshold": threshold,
                    "test_n": len(model_test),
                    **score(model_test, threshold),
                })
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation", required=True)
    parser.add_argument("--test", required=True)
    parser.add_argument("--output", default="matched_far_results.csv")
    parser.add_argument("--budgets", default="0.01,0.005,0.001,0.0005")
    args = parser.parse_args()
    validation = pd.read_csv(args.validation)
    test = pd.read_csv(args.test)
    result = evaluate(validation, test, [float(item) for item in args.budgets.split(",")])
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    print(result.to_string(index=False))
    print(json.dumps({"status": "SCORED_SUPPLIED_FILES", "rows": int(len(result))}))


if __name__ == "__main__":
    main()
