"""Counts and projections from the executed training notebooks.

The CICIoT2023 confusion counts are the cells printed by ciciot23-final.ipynb.
CICDDoS2019 percentages are the comparison table printed by cicddos2019-final.ipynb.
Nothing here retrains a model, chooses a new threshold, or estimates duplicate overlap.
"""
from __future__ import annotations

import math

BENIGN_FLOWS_PER_DAY = 10_000_000
P_BENIGN_TRAIN = 129_538 / (129_538 + 5_362_433)
P_ATTACK_BENCHMARK = 1.0 - P_BENIGN_TRAIN

# First 500 batches of 512 on the unshuffled CICIoT2023 test loader.
DEEP_WINDOWS = 256_000
DEEP_BENIGN = 5_962
DEEP_ATTACK = 250_038
# Stratified classical sample, seed 42. Not the same rows as the windows above.
ML_TEST = 300_000
ML_BENIGN = 7_064
ML_ATTACK = 292_936

HYBRID = "TPE-tuned CNN–LSTM"
RF = "Random Forest"
COST_RATIOS = (0.1, 1.0, 10.0, 100.0)


def _clopper_pearson(successes: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Two-sided Clopper–Pearson interval as a proportion.

    Windows of stride 1 overlap, so this interval is too narrow for the deep models.
    It is reported as a binomial illustration of a single count, not as a repeated-run interval.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if successes < 0 or successes > n:
        raise ValueError("successes must lie between 0 and n")
    lower = 0.0 if successes == 0 else _beta_ppf(alpha / 2.0, successes, n - successes + 1)
    upper = 1.0 if successes == n else _beta_ppf(1.0 - alpha / 2.0, successes + 1, n - successes)
    return lower, upper


def _beta_ppf(p: float, a: float, b: float) -> float:
    if p <= 0.0:
        return 0.0
    if p >= 1.0:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if _regularized_beta(mid, a, b) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _regularized_beta(x: float, a: float, b: float) -> float:
    """Regularized incomplete beta I_x(a, b), continued fraction as in Numerical Recipes."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    if x > (a + 1.0) / (a + b + 2.0):
        return 1.0 - _regularized_beta(1.0 - x, b, a)
    log_front = (
        a * math.log(x)
        + b * math.log(1.0 - x)
        - (math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b))
        - math.log(a)
    )
    front = math.exp(log_front)
    c = 1.0
    d = 1.0 - (a + b) * x / (a + 1.0)
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, 200):
        numerator = m * (b - m) * x / ((a + 2 * m - 1) * (a + 2 * m))
        d = 1.0 + numerator * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + numerator / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        h *= d * c
        numerator = -(a + m) * (a + b + m) * x / ((a + 2 * m) * (a + 2 * m + 1))
        d = 1.0 + numerator * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + numerator / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-12:
            break
    return front * h


def _from_counts(name: str, tn: int, fp: int, fn: int, tp: int, roc: float, pr: float, train_s: float, infer_s: float, unit: str) -> dict:
    benign = tn + fp
    attack = fn + tp
    far = fp / benign
    fnr = fn / attack
    tpr = tp / attack
    precision = tp / (tp + fp)
    f1 = 0.0 if precision + tpr == 0 else 2 * precision * tpr / (precision + tpr)
    far_lo, far_hi = _clopper_pearson(fp, benign)
    return {
        "Model": name,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "TP": tp,
        "N": tn + fp + fn + tp,
        "Benign": benign,
        "Attack": attack,
        "Unit": unit,
        "Acc": 100.0 * (tn + tp) / (tn + fp + fn + tp),
        "Prec": 100.0 * precision,
        "Rec": 100.0 * tpr,
        "F1": 100.0 * f1,
        "Spec": 100.0 * tn / benign,
        "ROC": 100.0 * roc,
        "PR": 100.0 * pr,
        "FAR": 100.0 * far,
        "FNR": 100.0 * fnr,
        "FAR_lo": 100.0 * far_lo,
        "FAR_hi": 100.0 * far_hi,
        "Train_s": train_s,
        "Infer_s": infer_s,
    }


# Confusion matrices printed by the CICIoT2023 notebook. ROC and PR areas use the
# softmax attack probability; the reported decision itself is the two-class argmax.
CICIOT = [
    _from_counts("CNN Only", 5957, 5, 4067, 245971, 0.9961596961045885, 0.9999091896030486, 262.8894443511963, 4.5767645835876465, "window"),
    _from_counts("LSTM Only", 5954, 8, 3776, 246262, 0.9968329812191259, 0.9999250683389412, 472.75939178466797, 8.560029983520508, "window"),
    _from_counts(HYBRID, 5961, 1, 3820, 246218, 0.9962775517229063, 0.9999119368038163, 1642.8197433948517, 15.020688772201538, "window"),
    _from_counts("Logistic Regression", 7041, 23, 7443, 285493, 0.993794, 0.999851, 7.297142, 0.027905, "record"),
    _from_counts("Gaussian Naive Bayes", 7054, 10, 67879, 225057, 0.992178, 0.999794, 0.207270, 0.168317, "record"),
    _from_counts("Decision Tree", 6365, 699, 580, 292356, 0.949534, 0.997573, 4.602397, 0.016037, "record"),
    _from_counts(RF, 6633, 431, 496, 292440, 0.999593, 0.999990, 25.650570, 0.390614, "record"),
    _from_counts("Hist. Gradient Boosting", 6637, 427, 779, 292157, 0.999352, 0.999984, 6.469641, 1.966381, "record"),
]

# Unique non-negative integers that reproduce the printed six-decimal precision,
# recall, and Matthews correlation, given the printed class supports.
# Classical support is 10,663 benign and 52,383 attack records.
# Deep support is 10,650 benign and 52,297 attack windows.
# These are not a saved confusion-matrix file.
CICDDOS_COUNTS = {
    "Decision Tree": (10662, 1, 1, 52382),
    "Extra Trees": (10662, 1, 3, 52380),
    "Random Forest": (10663, 0, 4, 52379),
    "LSTM Only": (10642, 8, 13, 52284),
    "CNN Only": (10622, 28, 5, 52292),
    "TPE-tuned CNN–LSTM": (10631, 19, 15, 52282),
    "Logistic Regression": (10567, 96, 485, 51898),
    "Gaussian Naive Bayes": (10291, 372, 2369, 50014),
}

# Printed comparison table. Deep-model fit times were not in that table.
CICDDOS = [
    {"Model": "Decision Tree", "Acc": 99.9968, "Prec": 99.9981, "Rec": 99.9981, "F1": 99.9981, "MCC": 0.999887, "ROC": 99.9944, "PR": 99.9978, "Train_s": 4.272066},
    {"Model": "Extra Trees", "Acc": 99.9937, "Prec": 99.9981, "Rec": 99.9943, "F1": 99.9962, "MCC": 0.999774, "ROC": 100.0000, "PR": 100.0000, "Train_s": 15.543884},
    {"Model": "Random Forest", "Acc": 99.9937, "Prec": 100.0000, "Rec": 99.9924, "F1": 99.9962, "MCC": 0.999774, "ROC": 100.0000, "PR": 100.0000, "Train_s": 21.161815},
    {"Model": "LSTM Only", "Acc": 99.9666, "Prec": 99.9847, "Rec": 99.9751, "F1": 99.9799, "MCC": 0.998814, "ROC": 99.9999, "PR": 100.0000, "Train_s": None},
    {"Model": "CNN Only", "Acc": 99.9476, "Prec": 99.9465, "Rec": 99.9904, "F1": 99.9685, "MCC": 0.998134, "ROC": 99.9994, "PR": 99.9999, "Train_s": None},
    {"Model": HYBRID, "Acc": 99.9460, "Prec": 99.9637, "Rec": 99.9713, "F1": 99.9675, "MCC": 0.998078, "ROC": 99.9989, "PR": 99.9998, "Train_s": None},
    {"Model": "Logistic Regression", "Acc": 99.0785, "Prec": 99.8154, "Rec": 99.0741, "F1": 99.4434, "MCC": 0.967907, "ROC": 99.6491, "PR": 99.9337, "Train_s": 5.697430},
    {"Model": "Gaussian Naive Bayes", "Acc": 95.6524, "Prec": 99.2617, "Rec": 95.4775, "F1": 97.3329, "MCC": 0.860792, "ROC": 98.7851, "PR": 99.7113, "Train_s": 0.218888},
]


def _attach_cicddos_counts() -> None:
    for row in CICDDOS:
        tn, fp, fn, tp = CICDDOS_COUNTS[row["Model"]]
        benign, attack = tn + fp, fn + tp
        row.update({
            "TN": tn,
            "FP": fp,
            "FN": fn,
            "TP": tp,
            "Benign": benign,
            "Attack": attack,
            "Unit": "window" if row["Model"] in {"CNN Only", "LSTM Only", HYBRID} else "record",
            "FAR": 100.0 * fp / benign,
            "FNR": 100.0 * fn / attack,
        })
        far_lo, far_hi = _clopper_pearson(fp, benign)
        row["FAR_lo"] = 100.0 * far_lo
        row["FAR_hi"] = 100.0 * far_hi


_attach_cicddos_counts()


def by_name(name: str) -> dict:
    for row in CICIOT:
        if row["Model"] == name:
            return row
    raise KeyError(name)


def precision_at_pi(tpr: float, far: float, pi: float) -> float:
    den = tpr * pi + far * (1.0 - pi)
    if den <= 0:
        return float("nan")
    return (tpr * pi) / den


def expected_cost(far: float, fnr: float, pi: float, ratio: float, c_fp: float = 1.0) -> float:
    return c_fp * far * (1.0 - pi) + (c_fp * ratio) * fnr * pi


def rate_gaps() -> tuple[float, float]:
    """Return (delta FAR, delta FNR) as proportions from the exact evaluated counts."""
    hybrid = by_name(HYBRID)
    forest = by_name(RF)
    return (forest["FAR"] - hybrid["FAR"]) / 100.0, (hybrid["FNR"] - forest["FNR"]) / 100.0


def crossover_prevalence(ratio: float) -> float:
    """Attack prevalence below which the hybrid has the lower expected cost of the two points."""
    d_far, d_fnr = rate_gaps()
    return d_far / (d_far + ratio * d_fnr)


def false_alerts(far_pct: float, benign_flows: float = BENIGN_FLOWS_PER_DAY) -> float:
    return (far_pct / 100.0) * benign_flows


def never_alert_prevalence(ratio: float, far: float, tpr: float) -> float:
    return far / (far + ratio * tpr)


def always_alert_prevalence(ratio: float, far: float, fnr: float) -> float:
    gap = 1.0 - far
    return gap / (gap + ratio * fnr)


def roc_hull_labels() -> list[str]:
    """Upper ROC convex hull of the eight evaluated points plus the two trivial policies."""
    points = [(0.0, 0.0, "never alert")]
    for row in CICIOT:
        points.append((row["FAR"] / 100.0, row["Rec"] / 100.0, row["Model"]))
    points.append((1.0, 1.0, "always alert"))
    current = points[0]
    hull = [current[2]]
    unused = points[1:]
    while current[2] != "always alert":
        best = None
        best_slope = None
        for far, tpr, name in unused:
            dfar = far - current[0]
            if dfar < -1e-15:
                continue
            if dfar <= 1e-15:
                slope = 1e9 if tpr > current[1] + 1e-15 else -1e9
            else:
                slope = (tpr - current[1]) / dfar
            if best is None or slope > best_slope + 1e-9:
                best = (far, tpr, name)
                best_slope = slope
        if best is None:
            raise RuntimeError("ROC hull did not reach the always-alert policy")
        hull.append(best[2])
        current = best
        unused = [item for item in unused if item[2] != best[2]]
    return hull


def key_numbers() -> dict:
    hybrid = by_name(HYBRID)
    forest = by_name(RF)
    h_tpr, h_far = hybrid["Rec"] / 100.0, hybrid["FAR"] / 100.0
    r_tpr, r_far = forest["Rec"] / 100.0, forest["FAR"] / 100.0
    return {
        "hybrid_precision_1pct": 100 * precision_at_pi(h_tpr, h_far, 0.01),
        "rf_precision_1pct": 100 * precision_at_pi(r_tpr, r_far, 0.01),
        "hybrid_precision_0_1pct": 100 * precision_at_pi(h_tpr, h_far, 0.001),
        "rf_precision_0_1pct": 100 * precision_at_pi(r_tpr, r_far, 0.001),
        "crossover_equal_pct": 100 * crossover_prevalence(1.0),
        "far_fold": forest["FAR"] / hybrid["FAR"],
        "alerts_hybrid": false_alerts(hybrid["FAR"]),
        "alerts_rf": false_alerts(forest["FAR"]),
        "alerts_hybrid_ci_low": false_alerts(hybrid["FAR_lo"]),
        "alerts_hybrid_ci_high": false_alerts(hybrid["FAR_hi"]),
        "delta_far_pct": forest["FAR"] - hybrid["FAR"],
        "delta_fnr_pct": hybrid["FNR"] - forest["FNR"],
        "hybrid_far_pct": hybrid["FAR"],
        "rf_far_pct": forest["FAR"],
        "hybrid_fnr_pct": hybrid["FNR"],
        "rf_fnr_pct": forest["FNR"],
        "hybrid_fp": hybrid["FP"],
        "hybrid_benign": hybrid["Benign"],
        "rf_fp": forest["FP"],
        "rf_benign": forest["Benign"],
        "hybrid_fn": hybrid["FN"],
        "rf_fn": forest["FN"],
        "far_ci_low_pct": hybrid["FAR_lo"],
        "far_ci_high_pct": hybrid["FAR_hi"],
    }


def _self_check() -> None:
    hybrid = by_name(HYBRID)
    forest = by_name(RF)
    assert hybrid["N"] == DEEP_WINDOWS and hybrid["Benign"] == DEEP_BENIGN
    assert forest["N"] == ML_TEST and forest["Benign"] == ML_BENIGN
    assert abs(P_ATTACK_BENCHMARK - 0.9764) < 1e-4
    # The printed two-decimal percentages are the rounded exact fractions.
    assert f"{hybrid['FAR']:.2f}" == "0.02"
    assert f"{forest['FAR']:.2f}" == "6.10"
    assert f"{hybrid['FNR']:.2f}" == "1.53"
    assert f"{forest['FNR']:.2f}" == "0.17"
    # One success in 5,962. Checked against an independent beta quantile.
    lo, hi = _clopper_pearson(1, 5962)
    assert abs(lo - 4.246520333438214e-06) < 1e-9
    assert abs(hi - 0.0009341676787629059) < 1e-9
    nums = key_numbers()
    assert 98.0 < nums["hybrid_precision_1pct"] < 98.6
    assert 14.0 < nums["rf_precision_1pct"] < 14.4
    assert 81.5 < nums["crossover_equal_pct"] < 82.0
    assert 360 < nums["far_fold"] < 370
    assert roc_hull_labels() == ["never alert", HYBRID, RF, "always alert"]
    ddos_h = next(row for row in CICDDOS if row["Model"] == HYBRID)
    ddos_f = next(row for row in CICDDOS if row["Model"] == RF)
    assert (ddos_f["FP"], ddos_f["FN"]) == (0, 4)
    assert (ddos_h["FP"], ddos_h["FN"]) == (19, 15)
    assert ddos_f["FAR"] < ddos_h["FAR"] and ddos_f["FNR"] < ddos_h["FNR"]
    assert ddos_f["FAR_hi"] < ddos_h["FAR_lo"]
    # The integers must reproduce the printed six-decimal precision and recall.
    assert f"{ddos_h['TP'] / (ddos_h['TP'] + ddos_h['FP']):.6f}" == "0.999637"
    assert f"{ddos_h['TP'] / ddos_h['Attack']:.6f}" == "0.999713"
    assert f"{ddos_f['TP'] / ddos_f['Attack']:.6f}" == "0.999924"
    pi_star = crossover_prevalence(1.0)
    below, above = pi_star - 0.01, pi_star + 0.01
    assert expected_cost(hybrid["FAR"] / 100, hybrid["FNR"] / 100, below, 1) < expected_cost(forest["FAR"] / 100, forest["FNR"] / 100, below, 1)
    assert expected_cost(forest["FAR"] / 100, forest["FNR"] / 100, above, 1) < expected_cost(hybrid["FAR"] / 100, hybrid["FNR"] / 100, above, 1)
    for ratio in COST_RATIOS:
        never = never_alert_prevalence(ratio, hybrid["FAR"] / 100, hybrid["Rec"] / 100)
        always = always_alert_prevalence(ratio, forest["FAR"] / 100, forest["FNR"] / 100)
        assert never < crossover_prevalence(ratio) < always
    # At the training mix and r = 100, always alerting is cheaper than random forest.
    pi = P_ATTACK_BENCHMARK
    assert (1.0 - pi) < expected_cost(forest["FAR"] / 100, forest["FNR"] / 100, pi, 100.0)


_self_check()
