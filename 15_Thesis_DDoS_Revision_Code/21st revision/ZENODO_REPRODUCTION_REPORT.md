# Zenodo reproduction

Internal note. Do not upload this file.

The public script was run from a clean folder that contained `code/*.py` and `metadata/botiot_results.json` plus `metadata/cicddos_subset_report.json`. The subset report was not placed beside the script.

Result: the script finished, and all 11 generated CSV files matched the deposited tables byte for byte.

`zenodo uploads/code/cicddos_subset_report.json` is absent. `zenodo uploads/metadata/cicddos_subset_report.json` is present. That is the intended layout.

The original CIC training run was not reproduced. The deposit rebuilds the derived tables.
