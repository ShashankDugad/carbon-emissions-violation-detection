# Carbon Emissions Violation Detection

Real-time anomaly detection system for carbon emissions violations using Apache Spark on 796M records from EPA and NOAA.

## Project Overview

- **Dataset**: 796M rows (EPA AQS 400M + NOAA LCD 396M)
- **Scale**: 2015-2024, 50 US states, 111GB Parquet
- **Tech Stack**: PySpark, HDFS, Python 3.9+
- **Platform**: NYU JupyterHub
- **Goal**: Predict emissions violations 24-48 hours in advance

## Project Structure
```
carbon-emissions-violation-detection/
├── data/
│   ├── raw/              # Original EPA/NOAA CSV files
│   ├── processed/        # Parquet files (partitioned)
│   └── sample/           # Small samples for testing
├── notebooks/
│   ├── exploration/      # EDA notebooks
│   ├── processing/       # Data pipeline notebooks
│   └── modeling/         # ML model notebooks
├── src/
│   ├── ingestion/        # Data download scripts
│   ├── preprocessing/    # Cleaning, schema validation
│   ├── analysis/         # Feature engineering, EDA
│   ├── models/           # ML model training/inference
│   └── utils/            # Helper functions
├── config/               # YAML configuration files
├── scripts/              # Bash automation scripts
├── tests/                # Unit and integration tests
├── docs/                 # Architecture and design docs
├── artifacts/            # Logs, metrics, reports
├── outputs/              # Final results and visualizations
├── requirements.txt      # Python dependencies
├── Makefile             # Automation commands
└── setup.py             # Package installation
```

## Quick Start
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/carbon-emissions-violation-detection.git
cd carbon-emissions-violation-detection

# Install dependencies
pip install -r requirements.txt

# Download sample data
make download-sample

# Run data validation
make validate

# Process sample data
make process-sample
```

## Data Sources

- **EPA AQS**: https://aqs.epa.gov/aqsweb/airdata/
- **NOAA LCD**: https://www.ncei.noaa.gov/data/local-climatological-data/

## Requirements

- Python 3.9+
- PySpark 3.5+
- 20GB+ disk space (for samples)
- NYU JupyterHub access (for full pipeline)

## Team

[Add your names and NetIDs]

## License

MIT License - see LICENSE file
```

**FILE: requirements.txt**
```
pyspark==3.5.1
pandas==2.2.2
numpy==1.26.4
requests==2.31.0
pyyaml==6.0.1
python-dotenv==1.0.1
matplotlib==3.8.4
seaborn==0.13.2
scikit-learn==1.4.2
pytest==8.1.1
black==24.3.0
flake8==7.0.0
