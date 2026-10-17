"""Rebuild the derived tables and figures from the stored rates.

    python reproduce_derived_analyses.py --tables ../tables --figures ../figures

The script does not train models. Matplotlib's bundled DejaVu font is used so the
graphical abstract does not depend on a Windows font path. Run it from any working
directory; the script adds its own folder to the import path.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import derived_metrics as dm

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 8,
    "axes.linewidth": 0.8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

HYBRID_COLOR = "#0072B2"
RF_COLOR = "#E69F00"


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _fmt(value, digits=2) -> str:
    return f"{value:.{digits}f}"


def _count_cell(value: float) -> str:
    """Avoid printing a reconstructed count of about 6 as 10."""
    if value < 10:
        return "< 10"
    return f"{dm.round_count(value):,}"


def _short(name: str) -> str:
    return {
        "TPE-tuned CNN–LSTM": "CNN–LSTM",
        "Hist. Gradient Boosting": "HGB",
        "Gaussian Naive Bayes": "NB",
        "Logistic Regression": "LR",
        "Decision Tree": "DT",
        "Random Forest": "RF",
        "CNN Only": "CNN",
        "LSTM Only": "LSTM",
        "Extra Trees": "ET",
    }.get(name, name)


def build_tables(table_dir: Path) -> None:
    t1 = [
        {"Study": "Ko et al. (2020)", "Focus": "Threshold moving for DDoS flood detection", "Relation": "Moves a threshold inside one detector"},
        {"Study": "Layeghy et al. (2024)", "Focus": "Synthetic versus operational NIDS benchmarks", "Relation": "Questions whether benchmark mixes match deployment"},
        {"Study": "Coscia et al. (2024)", "Focus": "Decision-tree rules for DoS and DDoS", "Relation": "Trees remain a deployable detector family"},
        {"Study": "Mittal et al. (2023)", "Focus": "Deep DDoS detection on CICDDoS2019", "Relation": "Architecture-centred use of the same benchmark"},
        {"Study": "Zhao et al. (2026)", "Focus": "Threshold-free anomaly detection", "Relation": "Avoids a fixed cut; this paper analyses the cut at 0.5"},
        {"Study": "González-Ramos et al. (2026)", "Focus": "Adversarial robustness of a hybrid NIDS", "Relation": "Evaluates evasion on CICIoT2023"},
        {"Study": "Wang et al. (2026a)", "Focus": "Imbalance-aware graph IDS", "Relation": "Changes the model rather than the operating-point reading"},
        {"Study": "Wang et al. (2026b)", "Focus": "Generative rebalancing for IIoT botnets", "Relation": "A different remedy for imbalance"},
        {"Study": "Lara-Gutierrez et al. (2026)", "Focus": "Class-specific GAN rebalancing", "Relation": "A different remedy for imbalance"},
        {"Study": "Hormozi et al. (2026)", "Focus": "Federated defence against multi-rate DDoS", "Relation": "A distributed defence, not an offline cost reading"},
        {"Study": "Javadpour et al. (2025)", "Focus": "Moving-target defence for edge IoT", "Relation": "Mitigation policy rather than detector scoring"},
        {"Study": "Rustam and Jurcut (2025)", "Focus": "Data drift in multi-environment networks", "Relation": "Distribution shift beyond a fixed prevalence"},
        {"Study": "This paper", "Focus": "Prevalence and cost reading of two executed operating points", "Relation": "Closed-form crossover of unequal slices; not a matched-threshold or alert-budget study"},
    ]
    _write_csv(table_dir / "Table1_JISA_positioning.csv", t1)

    t2 = [
        {
            "Dataset": "CICDDoS2019",
            "Train_records": "441,319",
            "Validation_records": "126,092",
            "Test_records": "63,046",
            "Scored_in_Section_5": "Trees: all 63,046 test records. Deep models: all 62,947 windows",
            "Features": "82, including a Unix timestamp",
            "Class_mix": "16.91% benign after capping each file’s attack rows at 5 times its benign rows",
            "Source": "Sharafaldin et al. (2019); CIC (2019)",
        },
        {
            "Dataset": "CICIoT2023",
            "Train_records": "5,491,971",
            "Validation_records": "1,176,851",
            "Test_records": "1,176,851",
            "Scored_in_Section_5": "Trees: 300,000 stratified test records. Deep models: first 256,000 of 1,176,752 windows",
            "Features": "46; every column except the label",
            "Class_mix": "Test file: 27,709 benign and 1,149,142 attack",
            "Source": "Neto et al. (2023); CIC (2023)",
        },
    ]
    _write_csv(table_dir / "Table2_Datasets.csv", t2)

    t3 = []
    for r in dm.CICDDOS:
        t3.append({
            "Model": r["Model"],
            "Unit": r["Unit"],
            "FP": f"{r['FP']:,}",
            "FN": f"{r['FN']:,}",
            "FAR_pct": f"{r['FAR']:.4f}",
            "FAR_CI95": f"{r['FAR_lo']:.3f}–{r['FAR_hi']:.3f}",
            "FNR_pct": f"{r['FNR']:.4f}",
            "F1_pct": _fmt(r["F1"]),
            "MCC": f"{r['MCC']:.4f}",
            "ROC_AUC_pct": _fmt(r["ROC"]),
        })
    _write_csv(table_dir / "Table3_CICDDoS2019_metrics.csv", t3)

    t4 = []
    for dataset, rows in (("CICDDoS2019", dm.CICDDOS), ("CICIoT2023", dm.CICIOT)):
        for r in rows:
            if r["Train_s"] is None:
                continue
            infer = r.get("Infer_s")
            t4.append({
                "Dataset": dataset,
                "Model": r["Model"],
                "Training_time_s": _fmt(r["Train_s"]),
                "Inference_time_s": "not recorded" if infer is None else _fmt(infer),
            })
    _write_csv(table_dir / "Table4_Training_times.csv", t4)

    t5 = [{
        "Model": r["Model"],
        "Accuracy_pct": _fmt(r["Acc"]),
        "Precision_pct": _fmt(r["Prec"]),
        "Recall_pct": _fmt(r["Rec"]),
        "F1_pct": _fmt(r["F1"]),
        "FAR_pct": _fmt(r["FAR"]),
        "FNR_pct": _fmt(r["FNR"]),
        "ROC_AUC_pct": _fmt(r["ROC"]),
        "PR_AUC_pct": _fmt(r["PR"]),
    } for r in dm.CICIOT]
    _write_csv(table_dir / "Table5_CICIoT2023_metrics.csv", t5)

    t6 = []
    for r in dm.CICIOT:
        t6.append({
            "Model": r["Model"],
            "Unit": r["Unit"],
            "Evaluated_cases": f"{r['N']:,}",
            "Benign_cases": f"{r['Benign']:,}",
            "Attack_cases": f"{r['Attack']:,}",
            "TN": f"{r['TN']:,}",
            "FP": f"{r['FP']:,}",
            "FN": f"{r['FN']:,}",
            "TP": f"{r['TP']:,}",
            "FAR_pct": _fmt(r["FAR"], 4),
            "FNR_pct": _fmt(r["FNR"], 4),
        })
    _write_csv(table_dir / "Table6_Evaluated_counts.csv", t6)

    t7 = []
    for r in dm.CICIOT:
        tpr, far = r["Rec"] / 100.0, r["FAR"] / 100.0
        t7.append({
            "Model": r["Model"],
            "π = 97.64 %": _fmt(100 * dm.precision_at_pi(tpr, far, dm.P_ATTACK_BENCHMARK)),
            "π = 50 %": _fmt(100 * dm.precision_at_pi(tpr, far, 0.5)),
            "π = 10 %": _fmt(100 * dm.precision_at_pi(tpr, far, 0.1)),
            "π = 1 %": _fmt(100 * dm.precision_at_pi(tpr, far, 0.01)),
            "π = 0.1 %": _fmt(100 * dm.precision_at_pi(tpr, far, 0.001)),
        })
    _write_csv(table_dir / "Table7_Prevalence_precision.csv", t7)

    t8 = []
    for ratio in dm.COST_RATIOS:
        hybrid = dm.by_name(dm.HYBRID)
        forest = dm.by_name(dm.RF)
        pi_star = 100 * dm.crossover_prevalence(ratio)
        never = 100 * dm.never_alert_prevalence(ratio, hybrid["FAR"] / 100.0, hybrid["Rec"] / 100.0)
        always = 100 * dm.always_alert_prevalence(ratio, forest["FAR"] / 100.0, forest["FNR"] / 100.0)
        t8.append({
            "Cost ratio r": _fmt(ratio, 1),
            "Crossover prevalence (%)": _fmt(pi_star),
            "Cheaper learned detector below": "CNN–LSTM hybrid",
            "Cheaper learned detector above": "random forest",
            "Never alert cheaper below (%)": _fmt(never, 4 if never < 0.01 else (3 if never < 1 else 2)),
            "Always alert cheaper above (%)": _fmt(always),
        })
    _write_csv(table_dir / "Table8_Crossover_prevalence.csv", t8)
    t9, t10 = _botiot_tables()
    _write_csv(table_dir / "Table9_BoTIoT_seeds.csv", t9)
    _write_csv(table_dir / "Table10_BoTIoT_features.csv", t10)
    _write_csv(table_dir / "Table11_CICDDoS_subset_ablation.csv", _subset_table())


def _botiot_report() -> dict:
    here = Path(__file__).resolve().parent
    for candidate in (here / "botiot_results.json", here.parent / "metadata" / "botiot_results.json"):
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    raise SystemExit("botiot_results.json was not found beside the script or in ../metadata")


def _botiot_pair(config: str, seed: int, model: str, cut: str) -> tuple[int, int]:
    row = _botiot_report()["populations"]["all"]["configs"][config]["seeds"][str(seed)]["models"][model][cut]
    return int(row["fp"]), int(row["fn"])


def _shown(value: int):
    return f"{value:,}" if value >= 1000 else value


def _botiot_tables() -> tuple[list[dict], list[dict]]:
    models = (
        ("Decision Tree", "Decision tree"),
        ("Random Forest", "Random forest"),
        ("HistGradientBoosting", "Histogram boosting"),
        ("Logistic Regression", "Logistic regression"),
    )
    # These checks keep the manuscript sentences tied to the repaired-mirror result file.
    assert _botiot_pair("audited_flow", 42, "Decision Tree", "threshold_0.5") == (0, 175)
    assert _botiot_pair("audited_flow", 42, "Decision Tree", "at_most_one_validation_fp") == (0, 175)
    assert _botiot_pair("audited_plus_ports", 42, "Decision Tree", "threshold_0.5") == (0, 135)
    assert _botiot_pair("audited_flow", 42, "Random Forest", "at_most_one_validation_fp") == (1, 49)
    assert _botiot_pair("audited_flow", 7, "Decision Tree", "at_most_one_validation_fp") == (2, 75)
    assert _botiot_pair("audited_flow", 123, "Decision Tree", "at_most_one_validation_fp") == (1, 73)
    assert _botiot_pair("flow_plus_ip_aggregates", 42, "Decision Tree", "threshold_0.5") == (0, 38)
    table9 = []
    for model, label in models:
        fp42, fn42 = _botiot_pair("audited_flow", 42, model, "threshold_0.5")
        fp7, fn7 = _botiot_pair("audited_flow", 7, model, "threshold_0.5")
        fp123, fn123 = _botiot_pair("audited_flow", 123, model, "threshold_0.5")
        tuned_fp, tuned_fn = _botiot_pair("audited_flow", 42, model, "at_most_one_validation_fp")
        table9.append({
            "Model": label,
            "Seed_42_FP": fp42,
            "Seed_42_FN": _shown(fn42),
            "Seed_7_FP": fp7,
            "Seed_7_FN": _shown(fn7),
            "Seed_123_FP": fp123,
            "Seed_123_FN": _shown(fn123),
            "Seed42_tuned_FP": tuned_fp,
            "Seed42_tuned_FN": _shown(tuned_fn),
        })
    rows = (
        ("Flow only, 0.5 cut", "audited_flow", "threshold_0.5"),
        ("Flow only, tuned cut", "audited_flow", "at_most_one_validation_fp"),
        ("Flow plus ports, 0.5 cut", "audited_plus_ports", "threshold_0.5"),
        ("Flow plus IP aggregates, 0.5 cut", "flow_plus_ip_aggregates", "threshold_0.5"),
    )
    keys = ("Decision Tree", "Random Forest", "HistGradientBoosting", "Logistic Regression")
    prefixes = ("Tree", "Forest", "Boosting", "Logistic")
    table10 = []
    for label, config, cut in rows:
        record = {"Features": label}
        for model, prefix in zip(keys, prefixes):
            fp, fn = _botiot_pair(config, 42, model, cut)
            record[f"{prefix}_FP"] = fp
            record[f"{prefix}_FN"] = _shown(fn)
        table10.append(record)
    return table9, table10


def _subset_report_path() -> Path:
    here = Path(__file__).resolve().parent
    for candidate in (here / "cicddos_subset_report.json", here.parent / "metadata" / "cicddos_subset_report.json"):
        if candidate.exists():
            return candidate
    raise SystemExit("cicddos_subset_report.json was not found beside the script or in ../metadata")


def _subset_table() -> list[dict]:
    path = _subset_report_path()
    configs = json.loads(path.read_text(encoding="utf-8"))["configs"]
    full = configs["full_numeric"]["test_threshold_0.5"]
    timestamp = configs["no_timestamp"]["test_threshold_0.5"]
    inbound = configs["no_timestamp_inbound"]["test_threshold_0.5"]
    ports = configs["no_timestamp_inbound_ports"]["test_threshold_0.5"]
    assert (full["fp"], full["fn"]) == (timestamp["fp"], timestamp["fn"]) == (1, 3)
    assert (inbound["fp"], inbound["fn"]) == (1, 10)
    assert (ports["fp"], ports["fn"]) == (5, 18)
    rows = []
    for label, row in (
        ("Numeric columns", full),
        ("Without Inbound", inbound),
        ("Without Inbound and ports", ports),
    ):
        rows.append({
            "Features": label,
            "FP": row["fp"],
            "FN": row["fn"],
            "Benign": row["tn"] + row["fp"],
            "Attack": row["tp"] + row["fn"],
        })
    return rows


def _save(fig, folder: Path, stem: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    png = folder / f"{stem}.png"
    pdf = folder / f"{stem}.pdf"
    fig.savefig(png, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    image = Image.open(png).convert("RGB")
    image.save(folder / f"{stem}.tif", compression="tiff_lzw", dpi=(300, 300))


def build_figures(fig_dir: Path) -> None:
    _figure_protocol(fig_dir)
    _figure_reversal(fig_dir)
    _figure_operating_points(fig_dir)
    _figure_prevalence(fig_dir)
    _figure_boundary(fig_dir)
    _figure_botiot(fig_dir)
    _graphical_abstract(fig_dir)


def _figure_protocol(fig_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(11.8, 5.6))
    ax.axis("off")
    ax.set_xlim(0, 12.6)
    ax.set_ylim(0, 5.7)
    rows = [
        (3.15, "#E5F2EA", "CICDDoS2019", [
            "630,457 rows\nSort by timestamp\nKeep Unix time\nDrop IPs and Flow ID",
            "Medians of all rows\nbefore the split\nThen a random\n70 / 20 / 10 split",
            "MinMax scaler\nFit on training rows\nonly",
            "Trees: 300,000\ntraining rows,\nall 63,046 test records\nDeep: all 62,947 windows",
        ]),
        (0.35, "#E8F1FA", "CICIoT2023", [
            "Supplied split files\n5,491,971 · 1,176,851\n· 1,176,851\n46 columns, label out",
            "Missing values set to 0\ninside each split\nNo training-only median",
            "MinMax scaler\nFit on training rows\nonly",
            "Trees: 300,000\nstratified test records\nDeep: first 256,000\nof 1,176,752 windows",
        ]),
    ]
    for y, color, title, labs in rows:
        ax.text(0.15, y + 2.15, title, fontsize=8, fontweight="bold", va="center")
        xs = (1.55, 4.15, 6.75, 9.15)
        widths = (2.4, 2.4, 2.2, 3.15)
        for x, w, lab in zip(xs, widths, labs):
            ax.add_patch(plt.Rectangle((x, y), w, 2.05, facecolor=color, edgecolor="#222222", lw=0.8))
            ax.text(x + w / 2, y + 1.02, lab, ha="center", va="center", fontsize=7.2)
        for x0, x1 in ((3.95, 4.15), (6.55, 6.75), (8.95, 9.15)):
            ax.annotate(
                "",
                xy=(x1, y + 1.02),
                xytext=(x0, y + 1.02),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#222222"),
            )
    _save(fig, fig_dir, "Figure_01_protocol")


def _figure_reversal(fig_dir: Path) -> None:
    """False-alarm rates at the evaluated points, with binomial intervals."""
    ddos = {row["Model"]: row for row in dm.CICDDOS}
    iot_h = dm.by_name(dm.HYBRID)
    iot_f = dm.by_name(dm.RF)
    panels = [
        (
            "CICDDoS2019",
            "Same split; records versus windows",
            [
                ("Random forest", ddos[dm.RF], False),
                ("CNN–LSTM", ddos[dm.HYBRID], False),
            ],
            False,
        ),
        (
            "CICIoT2023",
            "Different cases; one cut",
            [
                ("CNN–LSTM", iot_h, True),
                ("Random forest", iot_f, True),
            ],
            True,
        ),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.4))
    for ax, (title, note, series, log_scale) in zip(axes, panels):
        for index, (label, row, _log) in enumerate(series):
            color = RF_COLOR if "forest" in label else HYBRID_COLOR
            far, lo, hi = row["FAR"], row["FAR_lo"], row["FAR_hi"]
            if far <= 0:
                ax.plot([index], [hi], marker="v", color=color, ms=8, zorder=3)
                ax.plot([index, index], [0, hi], color=color, lw=1.4, zorder=2)
                ax.annotate("0 observed", (index, hi), textcoords="offset points", xytext=(10, 6), fontsize=8, color=color)
            else:
                ax.errorbar(
                    [index],
                    [far],
                    yerr=[[max(far - lo, 0.0)], [max(hi - far, 0.0)]],
                    fmt="o",
                    color=color,
                    ms=8,
                    capsize=4,
                    lw=1.4,
                    zorder=3,
                )
                if log_scale and far > 1:
                    ax.annotate(
                        f"{lo:.2f}–{hi:.2f}",
                        (index, far),
                        textcoords="offset points",
                        xytext=(8, -14),
                        fontsize=8,
                        color=color,
                    )
        ax.set_xlim(-0.55, 1.55)
        ax.set_xticks([0, 1])
        ax.set_xticklabels([label for label, _row, _log in series], fontsize=9)
        ax.set_xlabel(note, fontsize=8)
        ax.set_title(title, fontsize=11)
        ax.set_ylabel("False-alarm rate (%)")
        ax.grid(True, axis="y", alpha=0.3)
        if log_scale:
            ax.set_yscale("log")
            ax.set_ylim(0.00015, 20)
        else:
            ax.set_ylim(0, 0.45)
    fig.tight_layout()
    _save(fig, fig_dir, "Figure_02_reversal")


def _figure_operating_points(fig_dir: Path) -> None:
    colors = {
        "CNN Only": "#56B4E9",
        "LSTM Only": "#009E73",
        dm.HYBRID: HYBRID_COLOR,
        "Logistic Regression": "#666666",
        "Gaussian Naive Bayes": "#000000",
        "Decision Tree": "#CC79A7",
        dm.RF: RF_COLOR,
        "Hist. Gradient Boosting": "#D55E00",
    }
    offsets = {
        "CNN Only": (6, 6),
        "LSTM Only": (6, -10),
        dm.HYBRID: (-28, 8),
        "Logistic Regression": (6, 4),
        "Gaussian Naive Bayes": (6, 4),
        "Decision Tree": (6, -8),
        dm.RF: (-14, 8),
        "Hist. Gradient Boosting": (6, 6),
    }
    hull = {dm.HYBRID, dm.RF}
    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    hybrid = dm.by_name(dm.HYBRID)
    forest = dm.by_name(dm.RF)
    fars = np.linspace(hybrid["FAR"], forest["FAR"], 80)
    tpr = hybrid["Rec"] + (forest["Rec"] - hybrid["Rec"]) * (fars - hybrid["FAR"]) / (forest["FAR"] - hybrid["FAR"])
    ax.plot(fars, 100.0 - tpr, color="#111111", lw=1.3, zorder=2, label="ROC convex-hull edge")
    labeled_interval = False
    for row in dm.CICIOT:
        ax.errorbar(
            row["FAR"],
            row["FNR"],
            xerr=[[row["FAR"] - row["FAR_lo"]], [row["FAR_hi"] - row["FAR"]]],
            fmt="none",
            ecolor="#0072B2" if row["Model"] == dm.HYBRID else "#888888",
            elinewidth=1.3 if row["Model"] == dm.HYBRID else 0.8,
            capsize=3,
            zorder=4,
            label="95% binomial interval" if not labeled_interval else None,
        )
        labeled_interval = True
    for row in dm.CICIOT:
        on_hull = row["Model"] in hull
        ax.scatter(
            row["FAR"],
            row["FNR"],
            s=64 if on_hull else 42,
            color=colors[row["Model"]] if on_hull else "#8A8A8A",
            zorder=4 if on_hull else 3,
        )
        ax.annotate(
            _short(row["Model"]),
            (row["FAR"], row["FNR"]),
            textcoords="offset points",
            xytext=offsets[row["Model"]],
            fontsize=8,
            color="#111111" if on_hull else "#555555",
        )
    # Equal-cost line at 1% prevalence through the hybrid. On this scale it sits
    # immediately left of the tree models: beyond it, a detector costs more than
    # the hybrid even if it misses no attacks.
    pi, ratio = 0.01, 1.0
    c_h = dm.expected_cost(hybrid["FAR"] / 100, hybrid["FNR"] / 100, pi, ratio)
    far_cap = 100.0 * c_h / (1.0 - pi)  # percent; FNR = 0
    ax.axvline(far_cap, color=HYBRID_COLOR, ls="--", lw=1.0, zorder=1)
    ax.text(
        far_cap * 1.15,
        12,
        "Equal-cost bound\nat 1% prevalence",
        color=HYBRID_COLOR,
        fontsize=8,
        va="top",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("False-alarm rate at the reported cut (%)")
    ax.set_ylabel("Miss rate at the reported cut (%)")
    ax.set_xlim(0.0002, 30)
    ax.set_ylim(0.1, 40)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, loc="upper right")
    _save(fig, fig_dir, "Figure_03_operating_points")


def _figure_prevalence(fig_dir: Path) -> None:
    styles = {
        "CNN Only": ("#56B4E9", "-"),
        "LSTM Only": ("#009E73", "-"),
        dm.HYBRID: (HYBRID_COLOR, "-"),
        "Logistic Regression": ("#666666", "--"),
        "Gaussian Naive Bayes": ("#000000", ":"),
        "Decision Tree": ("#CC79A7", "-."),
        dm.RF: (RF_COLOR, "-"),
        "Hist. Gradient Boosting": ("#D55E00", "--"),
    }
    pis = np.logspace(np.log10(0.0005), np.log10(0.99), 400)
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    for row in dm.CICIOT:
        color, ls = styles[row["Model"]]
        ys = [100 * dm.precision_at_pi(row["Rec"] / 100, row["FAR"] / 100, pi) for pi in pis]
        ax.plot(100 * pis, ys, color=color, ls=ls, lw=1.8 if row["Model"] in {dm.HYBRID, dm.RF} else 1.2, label=_short(row["Model"]))
    ax.axvline(1.0, color="#444444", ls=":", lw=0.9, label="1% prevalence")
    ax.axvline(100 * dm.P_ATTACK_BENCHMARK, color="#222222", ls="--", lw=0.9, label="Training mix, 97.64%")
    ax.set_xscale("log")
    ax.set_xlim(0.05, 100)
    ax.set_ylim(0, 105)
    ax.set_xlabel("Attack prevalence (%)")
    ax.set_ylabel("Projected precision (%)")
    ax.legend(frameon=False, loc="center left", bbox_to_anchor=(1.02, 0.55))
    ax.grid(True, which="both", alpha=0.25)
    fig.subplots_adjust(right=0.78)
    _save(fig, fig_dir, "Figure_04_prevalence")


def _figure_boundary(fig_dir: Path) -> None:
    from matplotlib.patches import Patch

    hybrid = dm.by_name(dm.HYBRID)
    forest = dm.by_name(dm.RF)
    ratios = np.logspace(np.log10(0.05), np.log10(200), 500)
    pi_star = np.array([100 * dm.crossover_prevalence(r) for r in ratios])
    pi_never = np.array([
        100 * dm.never_alert_prevalence(r, hybrid["FAR"] / 100.0, hybrid["Rec"] / 100.0) for r in ratios
    ])
    pi_always = np.array([
        100 * dm.always_alert_prevalence(r, forest["FAR"] / 100.0, forest["FNR"] / 100.0) for r in ratios
    ])
    fig, ax = plt.subplots(figsize=(8.4, 5.3))
    ax.fill_between(ratios, 0, pi_never, color="#BDBDBD", zorder=1)
    ax.fill_between(ratios, pi_never, pi_star, color=HYBRID_COLOR, alpha=0.35, zorder=1)
    ax.fill_between(ratios, pi_star, np.minimum(pi_always, 100), color=RF_COLOR, alpha=0.45, zorder=1)
    ax.fill_between(ratios, np.minimum(pi_always, 100), 100, color="#7B3294", alpha=0.30, zorder=1)
    ax.plot(ratios, pi_star, color="#111111", lw=1.6, zorder=2)
    for ratio in dm.COST_RATIOS:
        star = 100 * dm.crossover_prevalence(ratio)
        ax.scatter([ratio], [star], color="#111111", s=28, zorder=3)
        offset = (8, -14) if ratio < 0.2 else (6, 8)
        ax.annotate(f"{star:.1f}%", (ratio, star), textcoords="offset points", xytext=offset, fontsize=8)
    ax.axhline(100 * dm.P_ATTACK_BENCHMARK, color="#444444", ls=":", lw=0.8, zorder=2)
    ax.set_xscale("log")
    ax.set_xlim(0.05, 200)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Miss cost / false-alarm cost  (assumed)")
    ax.set_ylabel("Attack prevalence (%)")
    handles = [
        Patch(facecolor="#BDBDBD", edgecolor="none", label="Never alert lower cost"),
        Patch(facecolor=HYBRID_COLOR, alpha=0.35, edgecolor="none", label="CNN–LSTM hybrid lower cost"),
        Patch(facecolor=RF_COLOR, alpha=0.45, edgecolor="none", label="Random forest lower cost"),
        Patch(facecolor="#7B3294", alpha=0.30, edgecolor="none", label="Always alert lower cost"),
    ]
    ax.legend(handles=handles, frameon=False, loc="center left", bbox_to_anchor=(1.02, 0.72))
    inset = ax.inset_axes([0.14, 0.18, 0.26, 0.26])
    inset.fill_between(ratios, 0, pi_never, color="#BDBDBD")
    inset.fill_between(ratios, pi_never, pi_star, color=HYBRID_COLOR, alpha=0.35)
    inset.fill_between(ratios, pi_star, np.minimum(pi_always, 100), color=RF_COLOR, alpha=0.45)
    inset.plot(ratios, pi_star, color="#111111", lw=1.1)
    inset.set_xscale("log")
    inset.set_yscale("log")
    inset.set_xlim(0.05, 200)
    inset.set_ylim(0.001, 10)
    inset.set_title("Below 10% prevalence", fontsize=8)
    inset.tick_params(labelsize=7)
    inset.set_facecolor("white")
    fig.subplots_adjust(right=0.72)
    _save(fig, fig_dir, "Figure_05_crossover")


def _figure_botiot(fig_dir: Path) -> None:
    """Seed-42 miss and false-alarm counts, read from the executed result file."""
    labels = ["Flow, 0.5", "Flow, tuned", "Ports, 0.5", "IP fields, 0.5"]
    specs = (
        ("Decision Tree", "Decision tree", "#CC79A7"),
        ("Random Forest", "Random forest", RF_COLOR),
        ("HistGradientBoosting", "Histogram boosting", "#009E73"),
        ("Logistic Regression", "Logistic regression", "#666666"),
    )
    cuts = (
        ("audited_flow", "threshold_0.5"),
        ("audited_flow", "at_most_one_validation_fp"),
        ("audited_plus_ports", "threshold_0.5"),
        ("flow_plus_ip_aggregates", "threshold_0.5"),
    )
    series = []
    for model, label, color in specs:
        misses, alarms = [], []
        for config, cut in cuts:
            fp, fn = _botiot_pair(config, 42, model, cut)
            alarms.append(fp)
            misses.append(fn)
        series.append((label, misses, alarms, color))
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.5))
    x = np.arange(len(labels))
    width = 0.18
    for ax, panel, ylabel, log_scale in (
        (axes[0], 0, "Missed attacks", True),
        (axes[1], 1, "False alarms", False),
    ):
        for index, (name, misses, alarms, color) in enumerate(series):
            values = misses if panel == 0 else alarms
            ax.bar(x + (index - 1.5) * width, values, width=width, color=color, label=name)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=15, ha="right")
        ax.set_ylabel(ylabel)
        ax.grid(True, axis="y", alpha=0.3)
        if log_scale:
            ax.set_yscale("log")
            ax.set_ylim(1, 50000)
        else:
            ax.set_ylim(0, 12)
    handles, legend_labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, legend_labels, frameon=False, fontsize=8, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 1.02))
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    _save(fig, fig_dir, "Figure_06_botiot")


def _graphical_abstract(fig_dir: Path) -> None:
    nums = dm.key_numbers()
    fig = plt.figure(figsize=(8.0, 3.0), dpi=300)
    fig.patch.set_facecolor("white")
    grid = fig.add_gridspec(1, 3, width_ratios=[1.05, 1.05, 1.2], wspace=0.28, left=0.04, right=0.98, top=0.78, bottom=0.16)
    fig.suptitle("At the evaluated points, the false-alarm order changes with the dataset", fontsize=11, fontweight="bold", y=0.94)

    left = fig.add_subplot(grid[0])
    left.axis("off")
    left.set_xlim(0, 1)
    left.set_ylim(0, 1)
    left.text(0.0, 0.92, "CICDDoS2019, same split", fontsize=8, fontweight="bold")
    for y, line in (
        (0.74, "Random forest"),
        (0.62, "0 false alarms in 10,663 records"),
        (0.50, "4 missed attacks"),
        (0.32, "CNN–LSTM hybrid"),
        (0.20, "19 false alarms in 10,650 windows"),
        (0.08, "15 missed attacks"),
    ):
        left.text(0.0, y, line, fontsize=8, color="#222222")

    mid = fig.add_subplot(grid[1])
    mid.axis("off")
    mid.set_xlim(0, 1)
    mid.set_ylim(0, 1)
    mid.text(0.0, 0.92, "CICIoT2023, different cases", fontsize=8, fontweight="bold")
    for y, line in (
        (0.74, "CNN–LSTM hybrid"),
        (0.62, "1 false alarm in 5,962 windows"),
        (0.50, "3,820 missed attacks"),
        (0.32, "Random forest"),
        (0.20, "431 false alarms in 7,064 records"),
        (0.08, "496 missed attacks"),
    ):
        mid.text(0.0, y, line, fontsize=8, color="#222222")

    right = fig.add_subplot(grid[2])
    pis = np.logspace(np.log10(0.001), np.log10(0.99), 300)
    for model, color, label in (
        (dm.HYBRID, HYBRID_COLOR, "CNN–LSTM"),
        (dm.RF, RF_COLOR, "Random forest"),
    ):
        row = dm.by_name(model)
        ys = [100 * dm.precision_at_pi(row["Rec"] / 100, row["FAR"] / 100, pi) for pi in pis]
        right.plot(100 * pis, ys, color=color, lw=2.0, label=label)
    right.axvline(1.0, color="#444444", ls="--", lw=0.8)
    right.set_xscale("log")
    right.set_ylim(0, 105)
    right.set_title("Projected if CICIoT rates stay fixed", fontsize=8)
    right.set_xlabel("Attack prevalence (%)", fontsize=8)
    right.set_ylabel("Projected precision (%)", fontsize=8)
    right.tick_params(labelsize=7)
    right.legend(frameon=False, fontsize=7, loc="lower right")
    right.grid(True, alpha=0.3)
    png = fig_dir / "Graphical_Abstract.png"
    tif = fig_dir / "Graphical_Abstract.tif"
    fig.savefig(png, dpi=300, facecolor="white")
    plt.close(fig)
    # Enforce the journal minimum width. The 8 in × 300 dpi canvas is 2400 px.
    image = Image.open(png).convert("RGB")
    if image.size[0] < 1328:
        raise SystemExit(f"Graphical abstract width {image.size[0]} is below 1328 px")
    image.save(tif, compression="tiff_lzw", dpi=(300, 300))
    image.save(png, dpi=(300, 300))


def write_all(table_dir: Path, fig_dir: Path) -> dict:
    build_tables(table_dir)
    build_figures(fig_dir)
    return dm.key_numbers()


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Rebuild derived DDoS evaluation tables and figures.")
    parser.add_argument("--tables", type=Path, default=here / "output" / "tables")
    parser.add_argument("--figures", type=Path, default=here / "output" / "figures")
    args = parser.parse_args()
    nums = write_all(args.tables, args.figures)
    print("tables", args.tables)
    print("figures", args.figures)
    print(
        f"precision@1% hybrid {nums['hybrid_precision_1pct']:.2f} "
        f"RF {nums['rf_precision_1pct']:.2f} crossover {nums['crossover_equal_pct']:.2f}"
    )


if __name__ == "__main__":
    main()
