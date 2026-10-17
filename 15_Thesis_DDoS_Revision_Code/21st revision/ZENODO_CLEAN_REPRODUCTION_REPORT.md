# Zenodo clean reproduction — Revision 21

## Method

1. Copied only `zenodo uploads/` into an isolated directory (no `_build` dependency).
2. Ran `code/reproduce_derived_analyses.py` with fresh `--tables` and `--figures`.
3. Byte-compared all deposited CSVs.

## Result

| Check | Outcome |
| --- | --- |
| CSV tables | **11/11** |
| Byte-identical | **11/11** |
| Printed projections | hybrid@1% = **98.34%**, RF@1% = **14.18%**, equal-cost crossover = **81.75%** |
| Figures generated | 20 files (not pixel-audited) |
| `cicddos_subset_report.json` | Loaded from `metadata/` |

## Interpretation

This verifies **derived-analysis reproducibility**, not original neural-network training. New revision-21 experimental artifacts (multi-attack predictions, RF+CNN ablation) are stored under `_experiments/new_results_r21/` and selected metadata JSON copies; they are **not** claimed to be inside the older interim DOI `10.5281/zenodo.23435601`.

Hash inventory: `ZENODO_FILE_INVENTORY.json`.
