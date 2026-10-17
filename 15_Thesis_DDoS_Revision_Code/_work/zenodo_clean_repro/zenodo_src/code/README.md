From this directory:

    python reproduce_derived_analyses.py --tables ../tables --figures ../figures

The script adds its own folder to the import path and uses Matplotlib’s DejaVu font. It rebuilds the prevalence, crossover, and alert figures from derived_metrics.py. Table 11 is read from ../metadata/cicddos_subset_report.json, and Tables 9 and 10 from ../metadata/botiot_results.json. run_botiot_audit.py retrains the BoT-IoT models when the official CSVs are supplied locally. Those CSVs are not included. Delete any __pycache__ directory before a public upload.

evaluate_saved_predictions.py computes miss rates at false-alarm budgets only when ../predictions/scores.csv exists, with columns model, split, y_true, y_score and an optional seed.
