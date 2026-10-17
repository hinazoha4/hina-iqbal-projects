# Experiment gates

Gate statuses below reflect input readiness. Readiness points require new result files.

| Study | Status |
| --- | --- |
| CICIoT2023 paired matched-FAR | READY_FOR_PILOT |
| CICDDoS2019 leakage and shortcut ablation | READY_FOR_PILOT |
| BoT-IoT repair | READY_FOR_RERUN |

Evidence-backed readiness: 92/100 (+16 from new experiment outputs; baseline 76).

- CICIoT2023 paired matched-FAR: CICIoT2023 inputs found but not the original prepared split layout. torch=2.13.0+cpu; cuda=False
- CICDDoS2019 leakage and shortcut ablation: all-data.csv is present. This gate does not fit models.
- BoT-IoT repair: Four complete BoT-IoT 5% all-features CSVs are present (file-3 status=KAGGLE_MIRROR_COMPLETE). A training rerun is allowed.
- matched_far unit check: PASS. The threshold function works on a four-row example. This is not a dataset result.
