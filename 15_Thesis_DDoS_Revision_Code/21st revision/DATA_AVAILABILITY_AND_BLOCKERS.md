# Data availability and blockers — Revision 21 feasibility

Generated 2026-10-17. No invented paths or checksums.

## Compute

| Resource | Status |
| --- | --- |
| Python / PyTorch | `torch 2.13.0+cpu` |
| CUDA | **Unavailable** (`cuda.is_available()=False`; Intel Iris Xe only) |
| Thesis notebooks path | `C:\Users\Lenovo\Downloads\New folder\thesis_notebooks` **missing** on this host |
| Historical Drive archives | CICIoT id `16ncVe5…` and CICDDoS id `1NcHRdcr…` return 404/HTML |

## Available inputs

| Asset | Path | Notes |
| --- | --- | --- |
| CICIoT multi-attack CSVs | `extracted/17th revision/data/ciciot2023/hf_ciciot_multi/` | HF `baalajimaestro/DDoS-CICIoT2023`; Benign + 10 DDoS families |
| CICIoT ICMP-only prior | `…/hf_ciciot/` | Prior S2 pilot source |
| CICDDoS `all-data.csv` | `…/cicddos2019/all-data.csv` (61,295,129 B; 120,444 rows) | Four-file subset; TFTP excluded |
| CICDDoS raw day files | `…/cicddos2019/hf_cicddos/01-12/` | Full day download present; large files OOM-risk |
| BoT-IoT Full5pc×4 | `…/botiot/UNSW_*.csv` | Complete Kaggle mirror; file3=285,316,035 B |
| Prior BoT results | `…/_experiments/new_results/botiot/botiot_results.json` | 350k stratified; 477 Normal; seeds 42/7/123 |
| Zenodo public package | `20th revision/…/zenodo uploads/` | Tables 1–11 metadata; derives without `_build` |

## Executable vs blocked

| Study | Feasible now? | Plan |
| --- | --- | --- |
| Zenodo derived reproduction | Yes | Clean isolated run (done) |
| Paired multi-attack CICIoT matched-FAR | **Yes (CPU pilot)** | HF multi-attack files; non-temporal windows documented |
| Original prepared-split CICIoT replication | **Blocked** | Private Drive archive absent |
| CICDDoS RF+CNN ablation on four-file subset | **Yes (CPU)** | Extend Table 11 with CNN–LSTM on same targets |
| CICDDoS full-day + hybrid Optuna | **Blocked / deferred** | Memory (TFTP ~8.8 GB) + no CUDA |
| BoT-IoT low-FAR precision | **Limited PASS** | Only 477 benign in source; FAR resolution ~1/72 |

## Recovery steps (if user supplies missing artifacts)

1. Place original `CICIOT23.zip` prepared `train/validation/test` under `data/ciciot2023/`.
2. Supply CUDA GPU host for full CNN–LSTM budgets.
3. Optionally rebuild `all-data.csv` including remaining day files on a high-RAM machine.
4. Official CloudStor BoT-IoT bytes remain preferred over Kaggle mirror when DNS/access allows.
