# JISA readiness assessment — post experiment gates (17 Oct 2026)

## Verdict

Provisional readiness: **86/100** (evidence-backed, with caveats).  
Automatic gate counter reached 92/100 after writing the three result files; the provisional score below discounts pilot/subset limitations that still prevent claiming a fully aligned replacement for the sixteenth-revision scientific claims.

Subjective acceptance prospect if submitted *with these new results and transparent limitations*: about **40–55%** (still major-revision territory at JISA, but materially stronger than 20–35%).

## Scorecard

| Dimension | Was (rev 17) | Now | Target | Notes |
| --- | ---: | ---: | ---: | --- |
| Original security contribution | 14/20 | 16/20 | 18/20 | Matched-FAR pilot shows protocol-dependent ordering |
| Methodological validity | 12/20 | 16/20 | 18/20 | Identical targets + val-only thresholds + leakage audit |
| Statistical robustness | 6/15 | 9/15 | 13/15 | One-seed CIC pilot; BoT-IoT benign n≈72 |
| Operational decision framework | 10/10 | 10/10 | 10/10 | Unchanged; still coherent |
| Reproducibility and transparency | 10/10 | 10/10 | 10/10 | New results stored separately; gates refuse invention |
| Literature and journal positioning | 9/10 | 9/10 | 9/10 | Unchanged |
| Editorial preparation | 15/15* | 14/15 | 14/15 | Author photos still missing |
| **Total** | **76** | **86** | **92** | |

\*Prior editorial score was coarse; missing photographs remain.

## What changed scientifically

1. **CICIoT2023 matched-FAR (PASS, pilot)** — RF and CNN–LSTM scored on identical `target_id`s; thresholds from validation only. At FAR budgets 0.001 and 0.0005, RF matched CNN–LSTM’s miss rate (FNR=0) with equal or fewer false alarms on this Benign vs ICMP-Flood subset.
2. **CICDDoS2019 leakage/shortcuts (PASS)** — Training-only imputation; 1,869 overlapping Flow IDs between train and test; port ablation worsens FAR/FNR.
3. **BoT-IoT (PASS, repaired source)** — Truncated file 3 refused; complete Kaggle mirror used; all 477 benign rows retained; seeds 42/7/123 completed under stratified subsample.

## What still blocks 90+

- Original private CICIoT prepared split and thesis checkpoints remain unavailable.
- CICIoT pilot is not yet a multi-attack, multi-seed, GPU full-budget study.
- CICDDoS `all-data.csv` excludes TFTP and other large day files (memory).
- BoT-IoT FAR resolution remains limited by ~71–72 test benigns.
- No NVIDIA CUDA on this host (`torch 2.13.0+cpu`, Intel Iris Xe only).

## Recommendation

Integrate the three new result tables into the manuscript as *protocol-corrected pilots*, keep historical fixed-threshold CIC tables clearly labeled as unreplicated operating points, fix the abstract CI wording for overlapping windows, then resubmit after (ideally) restoring the prepared CICIoT split and expanding CICDDoS coverage.
