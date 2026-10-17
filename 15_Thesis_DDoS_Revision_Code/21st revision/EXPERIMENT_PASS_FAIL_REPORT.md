# Experiment PASS / FAIL / BLOCKED — Revision 21

| Study | Status | Evidence |
| --- | --- | --- |
| Zenodo derived Tables 1–11 reproduction | **PASS** | Clean isolated run; 11/11 CSV byte-identical (`_experiments/zenodo_clean_repro/csv_byte_compare.json`) |
| CICIoT2023 paired multi-attack matched-FAR | **PASS (CPU pilot)** | Seeds 42 & 7; 11 families (Benign + 10 DDoS); identical `target_id`s; val-only thresholds; non-temporal windows documented |
| CICIoT2023 original prepared-split replication | **BLOCKED** | Private Drive archive absent; no CUDA |
| CICDDoS2019 RF+CNN–LSTM feature ablations | **PASS (four-file subset)** | Same targets; training-only imputation; Flow-ID overlap=1836; configs full→no ports |
| CICDDoS2019 full-day hybrid Optuna refit | **BLOCKED** | Memory (TFTP ~8.8 GB) + no CUDA |
| BoT-IoT repaired subsample | **PASS (limited)** | Complete file 3; 477 benign; seeds 42/7/123 prior JSON retained; FAR resolution ≈1/72 |

No scores, CIs, or confusion counts were invented.
