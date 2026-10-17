# What has to be supplied before the three studies can run

Internal note. Do not upload this file. Do not treat it as a result.

Place the files below, then run `python _experiments/run_gates.py` again. Training starts only after that command reports READY and a separate training script is written against those files.

1. CICIoT2023. Put the original train, validation, and test CSVs in `data/ciciot2023/`. A CUDA machine with PyTorch is also required for the CNN–LSTM pilot. This computer has neither the CSVs nor PyTorch.
2. CICDDoS2019. Put `all-data.csv` in `data/cicddos2019/`. The old official zip URL now returns the CIC dataset index page.
3. BoT-IoT. Replace file 3 with a copy that is exactly 282,131,555 bytes. The local copy is 268,435,456 bytes and must not be used as the complete source.

Until those files exist, the manuscript stays on the sixteenth-revision measurements and the readiness score stays 76/100.
