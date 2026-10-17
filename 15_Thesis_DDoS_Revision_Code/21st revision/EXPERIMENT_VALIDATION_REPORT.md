# Experiment validation

Internal note. Do not upload this file.

| Study | Status | Evidence |
| --- | --- | --- |
| Zenodo regeneration of Tables 1–11 | PASS | Clean run, 11/11 CSV byte matches |
| CICIoT2023 multi-attack paired comparison | BLOCKED | Original train/validation/test archive is not on this machine. CUDA does not see the GeForce MX450. Supplementary S2 remains a benign-versus-ICMP-flood pilot. |
| CICDDoS2019 hybrid refit on reduced features | BLOCKED | Table 11 is the existing four-file random-forest subset. The hybrid was not refit, and the remaining day files were not added. |
| BoT-IoT subsample | PASS as a limited study | Tables 9–10 come from the stored 350,000-row mirror subsample. Test benign support is 72 records at seed 42. No sub-0.1% false-alarm claim is made. |

No new model was trained for this revision.
