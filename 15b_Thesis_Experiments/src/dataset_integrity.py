"""Dataset integrity helpers. Never invent scores or labels."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

# Official published sizes from UNSW Full5pc all-features extract (botiot_source.md).
OFFICIAL_BOTIOT = {
    "UNSW_2018_IoT_Botnet_Full5pc_1.csv": 272_335_105,
    "UNSW_2018_IoT_Botnet_Full5pc_2.csv": 273_082_424,
    "UNSW_2018_IoT_Botnet_Full5pc_3.csv": 282_131_555,
    "UNSW_2018_IoT_Botnet_Full5pc_4.csv": 189_577_740,
}
TRUNCATED_FILE3 = 268_435_456

# Verified Kaggle mirror of the same 5% all-features extract (vigneshvenkateswaran/bot-iot-5-data).
# Schema matches Full5pc (46 columns including FLOW/PORTS/AGGREGATES/attack/category).
# Byte sizes differ from the published CloudStor copies; files parse to completion.
KAGGLE_BOTIOT_MIRROR = {
    "UNSW_2018_IoT_Botnet_Full5pc_1.csv": 277_543_651,
    "UNSW_2018_IoT_Botnet_Full5pc_2.csv": 278_451_723,
    "UNSW_2018_IoT_Botnet_Full5pc_3.csv": 285_316_035,
    "UNSW_2018_IoT_Botnet_Full5pc_4.csv": 191_754_639,
}

REQUIRED_BOTIOT_COLS = {
    "flgs_number", "proto_number", "pkts", "bytes", "state_number",
    "dur", "mean", "stddev", "sum", "min", "max",
    "spkts", "dpkts", "sbytes", "dbytes", "rate", "srate", "drate",
    "sport", "dport", "attack", "category",
}


def sha256_file(path: Path, limit: int | None = None) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        remaining = limit
        while True:
            chunk = handle.read(1024 * 1024 if remaining is None else min(1024 * 1024, remaining))
            if not chunk:
                break
            h.update(chunk)
            if remaining is not None:
                remaining -= len(chunk)
                if remaining <= 0:
                    break
    return h.hexdigest()


def ends_with_newline(path: Path) -> bool:
    with path.open("rb") as handle:
        handle.seek(0, 2)
        size = handle.tell()
        if size == 0:
            return False
        handle.seek(-1, 2)
        return handle.read(1) == b"\n"


def classify_botiot_file(path: Path) -> dict:
    size = path.stat().st_size
    official = OFFICIAL_BOTIOT.get(path.name)
    kaggle = KAGGLE_BOTIOT_MIRROR.get(path.name)
    status = "UNKNOWN"
    if official is not None and size == official:
        status = "OFFICIAL_BYTES"
    elif path.name.endswith("_3.csv") and size == TRUNCATED_FILE3:
        status = "TRUNCATED_REFUSED"
    elif kaggle is not None and size == kaggle:
        status = "KAGGLE_MIRROR_COMPLETE"
    elif official is not None and size > official * 0.95 and ends_with_newline(path):
        status = "COMPLETE_SIZE_MISMATCH"
    elif not ends_with_newline(path):
        status = "TRUNCATED_OR_PARTIAL"
    return {
        "name": path.name,
        "bytes": size,
        "official_bytes": official,
        "kaggle_mirror_bytes": kaggle,
        "ends_with_newline": ends_with_newline(path),
        "status": status,
    }


def botiot_gate(data_dir: Path) -> dict:
    files = []
    for name in OFFICIAL_BOTIOT:
        path = data_dir / name
        if not path.is_file():
            files.append({"name": name, "present": False, "bytes": None, "status": "MISSING"})
        else:
            info = classify_botiot_file(path)
            info["present"] = True
            files.append(info)
    third = next(item for item in files if item["name"].endswith("_3.csv"))
    if not third.get("present"):
        return {
            "study": "BoT-IoT repair",
            "status": "BLOCKED",
            "reason": "The third BoT-IoT CSV is not in the local data folder.",
            "files": files,
        }
    if third.get("status") == "TRUNCATED_REFUSED":
        return {
            "study": "BoT-IoT repair",
            "status": "FAIL",
            "reason": (
                f"File 3 is {third['bytes']} bytes. The published file is {OFFICIAL_BOTIOT[third['name']]} bytes. "
                "The truncated copy was not loaded."
            ),
            "files": files,
        }
    accepted = {"OFFICIAL_BYTES", "KAGGLE_MIRROR_COMPLETE", "COMPLETE_SIZE_MISMATCH"}
    if third.get("status") not in accepted:
        return {
            "study": "BoT-IoT repair",
            "status": "FAIL",
            "reason": f"File 3 status={third.get('status')} bytes={third.get('bytes')}.",
            "files": files,
        }
    present_ok = sum(1 for item in files if item.get("status") in accepted)
    if present_ok < 4:
        return {
            "study": "BoT-IoT repair",
            "status": "BLOCKED",
            "reason": f"Only {present_ok}/4 complete BoT-IoT CSVs accepted.",
            "files": files,
        }
    return {
        "study": "BoT-IoT repair",
        "status": "READY_FOR_RERUN",
        "reason": (
            "Four complete BoT-IoT 5% all-features CSVs are present "
            f"(file-3 status={third['status']}). A training rerun is allowed."
        ),
        "files": files,
        "provenance": (
            "Kaggle mirror vigneshvenkateswaran/bot-iot-5-data accepted when "
            "byte sizes match that mirror; official CloudStor sizes remain preferred."
        ),
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
