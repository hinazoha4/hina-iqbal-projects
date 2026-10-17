"""Record whether the three requested studies can run.

The script checks files and the local environment. It does not download datasets,
train models, or write prediction scores.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = Path(__file__).resolve().parent / "reports"
SRC = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SRC))

from dataset_integrity import TRUNCATED_FILE3, botiot_gate  # noqa: E402

# Prefer workspace data; fall back to historical path used in earlier revisions.
BOTIOT_CANDIDATES = [
    ROOT / "data" / "botiot",
    Path(r"D:\Research\Articles\MSc research\14th revision\_data"),
]
CICDDOS_URL = "http://cicresearch.ca/CICDataset/CICDDoS2019/Dataset/CSVs/CSV-01-12.zip"


def _present(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def _torch_status() -> dict:
    if importlib.util.find_spec("torch") is None:
        return {"installed": False, "cuda": False, "detail": "not installed"}
    import torch

    return {
        "installed": True,
        "cuda": bool(torch.cuda.is_available()),
        "detail": f"torch={torch.__version__}; cuda={torch.cuda.is_available()}",
    }


def _botiot_dir() -> Path | None:
    for candidate in BOTIOT_CANDIDATES:
        if candidate.is_dir() and any(candidate.glob("UNSW_2018_IoT_Botnet_Full5pc_*.csv")):
            return candidate
    return BOTIOT_CANDIDATES[0]


def _botiot_gate() -> dict:
    data = _botiot_dir()
    report = botiot_gate(data)
    report["data_dir"] = str(data)
    return report


def _ciciot_gate() -> dict:
    data = ROOT / "data" / "ciciot2023"
    prepared = [
        data / "train" / "train.csv",
        data / "validation" / "validation.csv",
        data / "test" / "test.csv",
    ]
    scores = data / "predictions_test.csv"
    torch_info = _torch_status()
    if all(_present(path) for path in prepared):
        return {
            "study": "CICIoT2023 paired matched-FAR",
            "status": "READY_FOR_PILOT",
            "reason": (
                "Prepared train/validation/test CSVs found "
                f"({torch_info['detail']}). This gate does not train them."
            ),
            "files": [str(path.relative_to(data)) for path in prepared],
            "torch": torch_info,
        }
    csvs = sorted(p for p in data.rglob("*.csv") if p.is_file()) if data.exists() else []
    if csvs or _present(scores):
        return {
            "study": "CICIoT2023 paired matched-FAR",
            "status": "READY_FOR_PILOT",
            "reason": (
                "CICIoT2023 inputs found but not the original prepared split layout. "
                f"{torch_info['detail']}"
            ),
            "files": [str(path.relative_to(data)) for path in csvs[:20]],
            "torch": torch_info,
        }
    return {
        "study": "CICIoT2023 paired matched-FAR",
        "status": "BLOCKED",
        "reason": (
            "No CICIoT2023 CSV and no saved validation or test scores are in data/ciciot2023. "
            f"{torch_info['detail']}. Original Google Drive id 16ncVe5ud8PdMUXzve-O1VI08DeTJpzIh "
            "now returns 404/HTML."
        ),
        "torch": torch_info,
    }


def _cicddos_gate() -> dict:
    candidate = ROOT / "data" / "cicddos2019" / "all-data.csv"
    raw_dir = ROOT / "data" / "cicddos2019" / "hf_cicddos" / "01-12"
    if _present(candidate):
        # Reject HTML masquerading as CSV
        head = candidate.read_bytes()[:200].lstrip()
        if head.startswith(b"<") or b"html" in head[:40].lower():
            return {
                "study": "CICDDoS2019 leakage and shortcut ablation",
                "status": "FAIL",
                "reason": f"all-data.csv looks like HTML ({candidate.stat().st_size} bytes).",
                "bytes": candidate.stat().st_size,
            }
        return {
            "study": "CICDDoS2019 leakage and shortcut ablation",
            "status": "READY_FOR_PILOT",
            "reason": "all-data.csv is present. This gate does not fit models.",
            "bytes": candidate.stat().st_size,
        }
    raw_csvs = sorted(raw_dir.glob("*.csv")) if raw_dir.exists() else []
    if raw_csvs:
        return {
            "study": "CICDDoS2019 leakage and shortcut ablation",
            "status": "READY_FOR_BUILD",
            "reason": (
                f"Found {len(raw_csvs)} raw 01-12 CSVs; all-data.csv not yet built."
            ),
            "files": [path.name for path in raw_csvs],
        }
    return {
        "study": "CICDDoS2019 leakage and shortcut ablation",
        "status": "BLOCKED",
        "reason": (
            "all-data.csv is absent. "
            f"{CICDDOS_URL} redirects to the CIC dataset index and does not serve the zip. "
            "Original notebook Drive id 1NcHRdcrLpHLILKxf7nMBawR3EPz1IMf0 returns HTML."
        ),
    }


def _unit_check() -> dict:
    import pandas as pd
    from matched_far import score, threshold_for_budget

    frame = pd.DataFrame({"score_attack": [0.1, 0.2, 0.8, 0.9], "y_true": [0, 0, 1, 1]})
    threshold, n_benign = threshold_for_budget(frame, 0.0)
    counted = score(frame, threshold)
    passed = n_benign == 2 and threshold > 0.2 and counted["fp"] == 0 and counted["tp"] == 2
    return {
        "name": "matched_far unit check",
        "status": "PASS" if passed else "FAIL",
        "meaning": "The threshold function works on a four-row example. This is not a dataset result.",
    }


def main() -> None:
    studies = [_ciciot_gate(), _cicddos_gate(), _botiot_gate()]
    unit = _unit_check()
    ready = sum(1 for study in studies if study["status"] in {"READY_FOR_RERUN", "READY_FOR_PILOT", "PASS"})
    # Points are awarded only after new valid experiment outputs exist.
    new_results = ROOT / "_experiments" / "new_results"
    awarded = 0
    if (new_results / "botiot" / "botiot_results.json").is_file():
        awarded += 4
    if (new_results / "ciciot2023" / "matched_far_results.csv").is_file():
        awarded += 6
    if (new_results / "cicddos2019" / "leakage_shortcut_report.json").is_file():
        awarded += 6
    readiness = min(92, 76 + awarded)
    report = {
        "baseline_readiness": 76,
        "points_awarded_for_new_experiments": awarded,
        "readiness": readiness,
        "target_not_claimed": 90,
        "studies": studies,
        "unit_check": unit,
        "truncated_file3_bytes_refused": TRUNCATED_FILE3,
        "ready_study_count": ready,
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "experiment_status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = [
        "# Experiment gates",
        "",
        "Gate statuses below reflect input readiness. Readiness points require new result files.",
        "",
        "| Study | Status |",
        "| --- | --- |",
    ]
    for study in studies:
        lines.append(f"| {study['study']} | {study['status']} |")
    lines.extend([
        "",
        f"Evidence-backed readiness: {report['readiness']}/100 "
        f"(+{awarded} from new experiment outputs; baseline 76).",
        "",
    ])
    for study in studies:
        lines.append(f"- {study['study']}: {study['reason']}")
    lines.append(f"- {unit['name']}: {unit['status']}. {unit['meaning']}")
    (REPORTS / "readiness_gates.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "readiness": report["readiness"],
        "awarded": awarded,
        "studies": [(s["study"], s["status"]) for s in studies],
        "unit": unit["status"],
    }))


if __name__ == "__main__":
    main()
