# Carbon Emissions Violation Detection

Real-time anomaly detection system for carbon emissions violations using Apache Spark on 796M records from EPA and NOAA.

## Project Overview

- **Dataset**: 796M rows (EPA AQS 400M + NOAA LCD 396M)
- **Scale**: 2015-2024, 50 US states, 111GB Parquet
- **Tech Stack**: PySpark, HDFS, Python 3.9+
- **Platform**: NYU JupyterHub
- **Goal**: Predict emissions violations 24-48 hours in advance

## Quick Start
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/carbon-emissions-violation-detection.git
cd carbon-emissions-violation-detection

# Setup project structure
make setup

# Install dependencies
make install

# Download sample data (5 EPA files + 10 NOAA stations)
make download-sample

# Validate data
make validate

# Process to Parquet
make process-sample
```

## Project Structure
```
carbon-emissions-violation-detection/
├── data/
│   ├── raw/              # Original CSV files
│   ├── processed/        # Parquet files (partitioned)
│   └── sample/           # Small samples for testing
├── notebooks/
│   ├── exploration/      # EDA notebooks
│   ├── processing/       # Data pipeline notebooks
│   └── modeling/         # ML model notebooks
├── src/
│   ├── ingestion/        # Data download scripts
│   ├── preprocessing/    # Cleaning, validation
│   ├── analysis/         # Feature engineering
│   ├── models/           # ML training/inference
│   └── utils/            # Helper functions
├── config/               # YAML configurations
├── scripts/              # Bash automation
├── tests/                # Unit tests
├── docs/                 # Documentation
├── artifacts/            # Logs, metrics, reports
├── outputs/              # Final results
├── Makefile              # Automation commands
└── requirements.txt      # Dependencies
```

## Data Sources

- **EPA AQS**: 400M rows, 5 pollutants (PM2.5, SO2, CO, NO2, O3), 2015-2024
  - Source: https://aqs.epa.gov/aqsweb/airdata/
- **NOAA LCD**: 396M rows, 2,953 weather stations, 2015-2024
  - Source: https://www.ncei.noaa.gov/data/local-climatological-data/

## Requirements

- Python 3.9+
- PySpark 3.5+
- 20GB+ disk (samples) / 150GB+ (full dataset)
- NYU JupyterHub access for production runs

## Development
```bash
# Run tests
make test

# Lint code
make lint

# Format code
make format

# Clean artifacts
make clean
```
## Team & Responsibilities

| Member | Role | Tasks (33% each) |
|--------|------|------------------|
| **Shashank** | Data Pipeline & ML Foundation | Environment setup, data acquisition (796M rows), HDFS/storage layout, schema validation, feature engineering, ML baseline model, GitHub repo structure, ingestion metrics |
| **Anshi** | Batch Processing & Analytics | Spark batch jobs, complex transformations (joins, aggregations), analytics queries at scale, performance optimization, timing comparisons, parameterized configs, unit tests, Makefile targets |
| **Ronit** | Streaming & Production | Kafka → Spark Structured Streaming pipeline, real-time simulation, streaming transformations, visual dashboard (Plotly/Streamlit), integration tests, CI/CD (GitHub Actions), architecture diagram, final presentation |

### Success Metrics
- ✓ Data scale: 796M rows (EPA 400M + NOAA 396M)
- ✓ Storage: Partitioned Parquet with 70% compression
- ⏳ Performance: Baseline vs optimized timing comparisons
- ⏳ ML Model: Baseline accuracy with training/inference metrics
- ⏳ Streaming: Real-time processing latency < 5 seconds
- ⏳ Reproducibility: One-command execution via Makefile
- ⏳ Code Quality: Unit tests, CI/CD passing, documentation

### Handoff Dependencies
```
SHASHANK (Data Pipeline) → ANSHI (Batch Processing) → RONIT (Streaming & Production)
     ↓                           ↓                              ↓
  Raw data in HDFS      Processed Parquet files      Final dashboard + CI/CD
```

## License

MIT License
