# S3 — Paired multi-attack CICIoT2023 matched-FAR pilot

## Protocol

- Source: Hugging Face `baalajimaestro/DDoS-CICIoT2023` (not the private thesis prepared split).
- Labels: filename-derived (Benign* → 0; DDoS-* → 1).
- Families used: BenignTraffic + ICMP Flood/Fragmentation, PSHACK, RSTFIN, SYN, SlowLoris, SynonymousIP, TCP Flood, UDP Flood/Fragmentation.
- Models: Random Forest (tabular) and CNN–LSTM (windows) on **identical** `target_id`s.
- Thresholds: selected on validation scores only; evaluated on held-out test IDs.
- Seeds: 42 and 7.
- Device: CPU (`torch 2.13.0+cpu`).

## Critical caveat

After stratified sampling, rows are **shuffled**. CNN–LSTM windows are therefore **non-temporal record sequences**. Do not interpret results as traffic time-series forecasting.

## Key result (seed 42, FAR budget 0.001)

| Model | FP | FN | FAR | FNR |
| --- | ---: | ---: | ---: | ---: |
| CNN–LSTM | 7 | 0 | 0.00672 | 0 |
| Random Forest | 3 | 0 | 0.00288 | 0 |

Full table: `02_Tables/Table12_CICIoT_multiattack_matched_FAR.csv`.
