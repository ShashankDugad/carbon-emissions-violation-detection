# Carbon Emissions Violation Detection

Real-time air quality violation prediction using 225M EPA + OpenAQ records on Apache Spark.

## Overview
**Problem:** Predict EPA air quality violations (PM2.5 > 35 µg/m³) to enable early interventions  
**Solution:** Random Forest classifier on 10 years of sensor data with 99.25% AUC  
**Platform:** NYU DataProc (HDFS + Spark 3.5, 3-node cluster)

## Dataset
- **Total Records:** 224,949,385 rows
  - EPA AQS: 221,980,963 (2015-2024)
  - OpenAQ: 2,968,422 (2023)
- **Storage:** 319.8 MB Parquet (from 51.7 GB CSV, 99.4% compression)
- **Pollutants:** Ozone, PM2.5, SO2, CO, NO2
- **Features:** 30 engineered (time, location, rolling averages)

## Results

### Model Performance
- **Algorithm:** Random Forest (50 trees, depth 10)
- **Validation AUC:** 99.40%
- **Test AUC:** 99.25%
- **Training Time:** 36 minutes on 30.6M samples

### Feature Importance
1. Current PM2.5 measurement: 52.35%
2. 7-day rolling average: 32.06%
3. Longitude: 7.94%
4. Month: 3.66%

### Key Findings
- California leads with 442,274 violations (2015-2024)
- PM2.5 levels decreased 12% from 2015-2019
- Time-based train/test split prevented data leakage

## Architecture
```
EPA API → CSV (51.7 GB) → HDFS → Spark → Parquet (320 MB)
                                    ↓
                          Feature Engineering (66M PM2.5 records)
                                    ↓
                          Random Forest → 99.25% AUC
```

## Pipeline Performance

| Phase | Input | Output | Time | Compression |
|-------|-------|--------|------|-------------|
| EPA Download | API | 43 GB CSV | 45 min | - |
| OpenAQ Download | S3 | 8.7 GB CSV | 20 min | - |
| Spark: CSV→Parquet | 51.7 GB | 319.8 MB | 5 min | 99.4% |
| Feature Engineering | 222M rows | 66M PM2.5 | 10 min | - |
| Model Training | 30.6M rows | RF model | 36 min | - |

## Repository Structure
```
carbon-emissions-violation-detection/
├── scripts/
│   ├── download_epa*.py          # Data ingestion
│   ├── convert_*_parquet*.py     # Spark preprocessing
│   ├── feature_engineering.py    # Feature creation
│   ├── train_baseline*.py        # ML training
│   ├── hyperparameter_tuning.py  # Model optimization
│   └── analytics_baseline.py     # EDA
├── artifacts/
│   ├── timing_table.md
│   ├── feature_importance.md
│   ├── hyperparameter_tuning.md
│   └── ml_results.md
├── logs/
│   └── session_*.md              # Daily progress logs
└── README.md
```


## How to Run This Project (Detailed Instructions)

### Prerequisites
- Apache Spark 3.5.3, Python 3.9+
- Access to NYU DataProc cluster or any Spark cluster with HDFS

### Setup
```bash
# Clone repository
git clone https://github.com/ShashankDugad/carbon-emissions-violation-detection.git
cd carbon-emissions-violation-detection

# View all available commands
make help
```

### Run Complete Pipeline
```bash
# Full ML pipeline (validation → analytics → features → training → importance)
make pipeline-full
# Duration: ~60 minutes
```

### Run Individual Components
```bash
make pipeline-validate     # Validate Parquet data (2 min)
make pipeline-features     # Feature engineering (10 min)
make pipeline-train        # Train Random Forest (36 min)
make batch-all             # Run all batch analytics
```

### Use Existing Data (Recommended)
```python
# Access pre-processed Parquet files directly
spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/features_pm25")
```

### Troubleshooting
- **Out of memory?** Increase `--executor-memory` in spark-submit commands
- **HDFS permission denied?** Run `hdfs dfs -chmod 755 /user/sd5957_nyu_edu/carbon_emissions/`
- **Full documentation:** See [PROJECT_REPORT.md](PROJECT_REPORT.md) Section 16

---



## Quick Start

### 1. Data Access (HDFS)
```bash
# Parquet files (read-only)
hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet/
hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/features_pm25/
```

### 2. Run Baseline Model
```bash
spark-submit \
  --driver-memory 8g \
  --executor-memory 12g \
  scripts/train_baseline_timesplit.py
```

### 3. Feature Importance
```bash
spark-submit scripts/feature_importance_optimized.py
```

## Team
- **Shashank Dugad (sd5957)** - Pipeline & ML
- **Anshi Shah (ans10020)** - Batch Processing
- **Ronit Gehani (rg4881)** - Streaming

## Technologies
- Apache Spark 3.5.3 (PySpark)
- HDFS (distributed storage)
- Random Forest (scikit-learn API)
- Parquet (columnar format)

## License
MIT

## Citations
- EPA Air Quality System: https://aqs.epa.gov/aqsweb/airdata/
- OpenAQ: https://openaq.org/
