# BoT-IoT source

Official page: https://research.unsw.edu.au/projects/bot-iot-dataset

Tables 9 and 10 are rebuilt from metadata/botiot_results.json. That file is a 350,000-row subsample of a Kaggle mirror of the 5% all-features extract (Koroniotis, Moustafa, Sitnikova and Turnbull, 2019). Every benign row is kept. The raw files are not included in this deposit.

The mirror byte lengths differ from the published CloudStor lengths:

| File | Published bytes | Mirror bytes |
| --- | ---: | ---: |
| UNSW_2018_IoT_Botnet_Full5pc_1.csv | 272335105 | 277543651 |
| UNSW_2018_IoT_Botnet_Full5pc_2.csv | 273082424 | 278451723 |
| UNSW_2018_IoT_Botnet_Full5pc_3.csv | 282131555 | 285316035 |
| UNSW_2018_IoT_Botnet_Full5pc_4.csv | 189577740 | 191754639 |

The mirror parses completely. It is not a byte-verified copy of the official files. An earlier truncated file of 268,435,456 bytes is not the source of Tables 9 and 10. Running code/run_botiot_audit.py on the full mirror will not reproduce those tables, because the deposited counts use the 350,000-row subsample.
