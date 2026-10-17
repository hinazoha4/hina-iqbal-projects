# S2. Paired-threshold pilot on a benign-versus-ICMP-flood subset

This file records a protocol check. It is not a reanalysis of the CICIoT2023 comparison in the manuscript.

The rows come from a Hugging Face copy of raw CICIoT2023 files, labelled from the file name. The classes are benign traffic and ICMP flood only. The draw is balanced, 60,000 rows, with 42,000 for training and 9,000 each for validation and test before windowing. The CNN–LSTM uses windows of 50 rows, two epochs, and a CPU. Random forest and the CNN–LSTM are scored on the same window targets. Thresholds are chosen on validation only. The seed is 42. The test set has 8,961 windows.

| Validation false-alarm budget | CNN–LSTM test false positives | Random forest test false positives | Test misses, both models |
| --- | ---: | ---: | ---: |
| 1.00% | 37 | 42 | 0 |
| 0.50% | 22 | 28 | 0 |
| 0.10% | 7 | 3 | 0 |
| 0.05% | 3 | 3 | 0 |

At the 0.10% validation budget the CNN–LSTM test false-alarm rate is 7 of 4,479 benign windows, about 0.156%, which exceeds the budget. Random forest has 3 false positives, about 0.067%. A threshold that meets the budget on validation can miss it on test.

Both models miss no attacks on this separable, balanced, single-attack subset. That result does not overturn the unpaired CICIoT2023 comparison, which uses the original attack mix and unequal slices.
