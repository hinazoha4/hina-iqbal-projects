# Supporting material

High F1, Costly Alerts: Dataset- and Prevalence-Dependent Rankings of Deep and Tree-Based DDoS Detectors

Version 1.0.0. This deposit rebuilds the paper’s prevalence, crossover, hull, and alert calculations from the confusion counts printed by the executed notebooks. It is not a training archive, and it does not reproduce the original model fits.

## Contents

- `tables/` — eleven tables
- `figures/` — PDF, PNG, and LZW TIFF
- `code/reproduce_derived_analyses.py` — rebuilds tables and figures from derived counts
- `code/run_botiot_audit.py` — retrains the BoT-IoT comparison when the official CSVs are available locally
- `code/evaluate_saved_predictions.py` — matched false-alarm evaluation when scores are supplied
- `predictions/` — empty until a score file is added
- `metadata/` — environment pins, BoT-IoT source note and results, literature screen

## Reproduce

From the deposit root, on Windows or Linux:

```
python code/reproduce_derived_analyses.py --tables tables_check --figures figures_check
```

Relative paths are enough. The script adds its own folder to the import path and draws figures with Matplotlib’s DejaVu Sans font.

## Licence

CC BY 4.0 for the derived tables, figures, and scripts. Raw CIC datasets are not included.

## Authors

Hina Iqbal, University of Coimbra, ORCID 0009-0002-2378-9414.
Cristiano Premebida, University of Coimbra, ORCID 0000-0002-2168-2077.
Usman Haider, Czech Technical University in Prague, ORCID 0000-0002-0125-0912.
