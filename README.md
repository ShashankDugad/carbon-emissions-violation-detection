# Carbon Emissions Violation Detection

Real-time prediction of air quality violations using 286M EPA records (2015-2024) on Apache Spark.

## Dataset
- **Rows:** 289,283,534 (44.6% over 200M target)
- **Size:** 51.7 GB raw CSV, ~15 GB Parquet (estimated)
- **Years:** 2015-2024 (10 years)
- **Pollutants:** Ozone (44201), PM2.5 (88101), SO2 (42401), CO (42101), NO2 (42602)
- **Platform:** NYU DataProc (HDFS + Spark 3.5)

## Status
✓ Data ingestion complete  
→ Next: Spark preprocessing, partitioning, baseline job

## Team
- Shashank Dugad (sd5957) - Pipeline & ML
- Anshi Shah (ans10020) - Batch Processing  
- Ronit Gehani (rg4881) - Streaming

## Repository
```
carbon-emissions-violation-detection/
├── scripts/
│   ├── download_epa.py
│   ├── download_epa_additional.py
│   ├── download_epa_2015-2017.py
│   └── download_openaq_*.py
├── logs/
│   ├── session_2025-10-27.md
│   └── session_2025-10-28.md
└── README.md
```

## Key Findings
- California leads with 442K violations
- PM2.5 levels decreased 12% (2015-2019)
- 99.4% storage reduction via Parquet

## Progress
✓ Data ingestion: 225M rows  
✓ Spark preprocessing: CSV → Parquet  
✓ Validation & analytics complete  
→ Next: Feature engineering, ML model
