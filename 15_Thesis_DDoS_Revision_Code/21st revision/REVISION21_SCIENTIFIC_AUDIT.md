# Revision 21 scientific audit

## What changed since revision 20

Revision 20 fixed Zenodo packaging (`cicddos_subset_report.json`) but trained no new models. Revision 21 executes the feasible scientific gates:

1. **Paired multi-attack CICIoT2023 matched-FAR (PASS, CPU pilot)**  
   - Families: BenignTraffic + 10 DDoS types (ICMP flood/frag, PSHACK, RSTFIN, SYN, SlowLoris, SynonymousIP, TCP, UDP flood/frag).  
   - Seeds 42 and 7; identical target IDs; thresholds from validation only.  
   - **Sequence caveat (required):** CNN–LSTM windows are **non-temporal shuffled-record sequences**, not chronologically ordered traffic.  
   - Finding: under tight matched FAR budgets, Random Forest often matches CNN–LSTM detection (FNR=0) with **fewer or equal false alarms** (e.g., seed 42 @ FAR≤0.001: RF FP=3 vs CNN–LSTM FP=7; both FNR=0). At the tightest 0.0005 budget both can reach 0 FP / 0 FN on this pilot.

2. **CICDDoS2019 RF + CNN–LSTM ablations (PASS on four-file subset)**  
   - Extends Table 11 beyond RF-only.  
   - Training-only median imputation; Flow-ID train/test overlap = **1836**.  
   - Port/Inbound removals degrade both models; CNN–LSTM remains weaker than RF at fixed 0.5 threshold on this subset—**do not** treat this as a universal deep-vs-tree ranking.

3. **BoT-IoT**  
   - Prior repaired complete-source subsample retained (477 benign; ~72 test benign at seed 42). No invented low-FAR precision.

4. **Zenodo derived reproduction**  
   - Reconfirmed 11/11 byte-identical CSVs in isolation.

## What remains blocked

- Original private CICIoT prepared split + CUDA full training.  
- Full-day CICDDoS (TFTP etc.) hybrid Optuna refit.  
- Author photographs.  
- New public Zenodo DOI for R21 artifacts.

## Novelty (honest)

The paired multi-attack matched-FAR pilot strengthens the **evaluation-protocol** contribution: detector preference can change when operating points are matched on identical targets across multiple attack families. It does **not** invent a new detector architecture. JISA incremental-AI exclusion risk is reduced relative to rev20 but not eliminated, because the pilot is CPU-scale, non-temporal for deep windows, and not the original thesis split.
