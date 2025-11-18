.PHONY: help setup install download-sample download-full validate process-sample process-full clean test lint format

# Variables
PYTHON := python3
PIP := pip3
EPA_BASE := https://aqs.epa.gov/aqsweb/airdata
NOAA_BASE := https://www.ncei.noaa.gov/data/local-climatological-data/access

help:
	@echo "  make help-pipeline   - Show ML pipeline commands"
	@echo "  make help-batch      - Show batch processing commands"
	@echo "=========================================="
	@echo "Carbon Emissions Detection - Make Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  make setup           - Create all directories and init files"
	@echo "  make install         - Install Python dependencies"
	@echo ""
	@echo "Data Commands:"
	@echo "  make download-sample - Download 5 EPA files + 10 NOAA stations"
	@echo "  make download-full   - Download all 50 EPA files + 2953 NOAA stations"
	@echo "  make validate        - Validate data schema and quality"
	@echo ""
	@echo "Processing Commands:"
	@echo "  make process-sample  - Convert sample data to Parquet"
	@echo "  make process-full    - Convert full dataset to Parquet (HPC only)"
	@echo ""
	@echo "Development Commands:"
	@echo "  make test            - Run unit tests"
	@echo "  make lint            - Run code linting"
	@echo "  make format          - Format code with black"
	@echo "  make clean           - Remove generated files"
	@echo ""

setup:
	@echo "Creating project structure..."
	mkdir -p data/{raw,processed,sample}
	mkdir -p notebooks/{exploration,processing,modeling}
	mkdir -p src/{ingestion,preprocessing,analysis,models,utils}
	mkdir -p config scripts tests docs artifacts/{logs,metrics,reports} outputs
	touch src/__init__.py
	touch src/ingestion/__init__.py
	touch src/preprocessing/__init__.py
	touch src/analysis/__init__.py
	touch src/models/__init__.py
	touch src/utils/__init__.py
	touch tests/__init__.py
	@echo "✓ Directory structure created"

install:
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt
	@echo "✓ Dependencies installed"

download-sample:
	@echo "Downloading EPA sample (5 files)..."
	bash scripts/download_epa_sample.sh
	@echo "Downloading NOAA sample (10 stations)..."
	bash scripts/download_noaa_sample.sh
	@echo "✓ Sample data downloaded to data/sample/"

download-full:
	@echo "WARNING: This will download ~115GB EPA + ~253GB NOAA data"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "Downloading all EPA files (50 files)..."
	bash scripts/download_epa_full.sh
	@echo "Downloading all NOAA stations (2953 stations)..."
	bash scripts/download_noaa_full.sh
	@echo "✓ Full dataset downloaded to data/raw/"

validate:
	@echo "Running data validation..."
	$(PYTHON) src/preprocessing/validate_schema.py
	$(PYTHON) src/preprocessing/data_quality_checks.py
	@echo "✓ Validation complete. Check artifacts/logs/validation.log"

process-sample:
	@echo "Processing sample data to Parquet..."
	$(PYTHON) src/preprocessing/convert_to_parquet.py --mode sample --input data/sample --output data/processed
	@echo "✓ Sample data processed to data/processed/"

process-full:
	@echo "Processing full dataset (requires Spark cluster)..."
	spark-submit \
		--master yarn \
		--deploy-mode client \
		--num-executors 10 \
		--executor-cores 4 \
		--executor-memory 8g \
		--driver-memory 4g \
		src/preprocessing/convert_to_parquet.py \
		--mode full \
		--input data/raw \
		--output data/processed
	@echo "✓ Full dataset processed"

test:
	@echo "Running tests..."
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=html
	@echo "✓ Tests complete. Coverage report in htmlcov/index.html"

lint:
	@echo "Running linters..."
	flake8 src/ tests/ --max-line-length=100
	@echo "✓ Linting complete"

format:
	@echo "Formatting code..."
	black src/ tests/ --line-length=100
	@echo "✓ Code formatted"

clean:
	@echo "Cleaning generated files..."
	rm -rf data/processed/*
	rm -rf artifacts/logs/*.log
	rm -rf artifacts/metrics/*
	rm -rf outputs/*
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleanup complete"

git-status:
	@git status

git-add:
	@git add -A
	@echo "✓ All changes staged"

git-commit:
	@read -p "Commit message: " msg; \
	git commit -m "$$msg"

git-push:
	@git push origin main
	@echo "✓ Pushed to GitHub"

commit-push: git-add git-commit git-push

# OpenAQ-specific commands
download-openaq-sample:
	@echo "Downloading OpenAQ sample (10 locations, 1 year)..."
	bash scripts/download_openaq_sample.sh
	@echo "✓ OpenAQ sample downloaded to data/sample/"

download-openaq-full:
	@echo "WARNING: This will download 1,178 locations × 5 years = ~21GB compressed"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ] || exit 1
	bash scripts/download_openaq_full.sh
	@echo "✓ OpenAQ data downloaded to data/raw/"

validate-openaq:
	@echo "Validating OpenAQ data structure..."
	$(PYTHON) src/preprocessing/validate_openaq_schema.py
	@echo "✓ OpenAQ validation complete"

# Update existing download-sample target
download-sample: download-openaq-sample

# Update help
.PHONY: download-openaq-sample download-openaq-full validate-openaq

# ==========================================
# ACTUAL PIPELINE (Completed Implementation)
# ==========================================

pipeline-validate:
	@echo "Validating Parquet data..."
	spark-submit scripts/validate_parquet.py

pipeline-analytics:
	@echo "Running baseline analytics..."
	spark-submit scripts/analytics_baseline.py

pipeline-features:
	@echo "Engineering features (PM2.5)..."
	spark-submit --driver-memory 8g --executor-memory 12g scripts/feature_engineering.py

pipeline-train:
	@echo "Training ML model (time-based split)..."
	spark-submit --driver-memory 8g --executor-memory 12g scripts/train_baseline_timesplit.py

pipeline-importance:
	@echo "Computing feature importance..."
	spark-submit --driver-memory 12g --executor-memory 16g --executor-cores 8 scripts/feature_importance_optimized.py

pipeline-tune:
	@echo "Hyperparameter tuning..."
	spark-submit --driver-memory 12g --executor-memory 16g scripts/hyperparameter_tuning.py

pipeline-full: pipeline-validate pipeline-analytics pipeline-features pipeline-train pipeline-importance

# HDFS paths (read-only for team)
show-data-paths:
	@echo "=== HDFS Data Locations ==="
	@echo "EPA Parquet: hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet/"
	@echo "OpenAQ Parquet: hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/openaq_parquet/"
	@echo "Features: hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/features_pm25/"
	@hdfs dfs -du -s -h /user/sd5957_nyu_edu/carbon_emissions/processed/

# Team data access
share-data:
	@echo "Setting read permissions for team..."
	hdfs dfs -chmod -R 755 /user/sd5957_nyu_edu/carbon_emissions/processed/
	@echo "✓ Team can now read Parquet files"

.PHONY: pipeline-validate pipeline-analytics pipeline-features pipeline-train pipeline-importance pipeline-tune pipeline-full show-data-paths share-data

help-pipeline:
	@echo ""
	@echo "=========================================="
	@echo "Completed ML Pipeline Commands"
	@echo "=========================================="
	@echo ""
	@echo "  make pipeline-validate    - Validate Parquet data quality"
	@echo "  make pipeline-analytics   - Run baseline analytics (violations by state)"
	@echo "  make pipeline-features    - Engineer ML features (time + location)"
	@echo "  make pipeline-train       - Train Random Forest (99.25% AUC)"
	@echo "  make pipeline-importance  - Compute feature importance"
	@echo "  make pipeline-tune        - Hyperparameter tuning"
	@echo "  make pipeline-full        - Run entire ML pipeline"
	@echo ""
	@echo "  make show-data-paths      - Display HDFS data locations"
	@echo "  make share-data           - Grant team read access to Parquet files"
	@echo ""

# Batch Processing Targets (Anshi's work)
batch-state-agg:
	@echo "Running state aggregations..."
	spark-submit --driver-memory 8g --executor-memory 12g scripts/batch_state_aggregations.py

batch-top-counties:
	@echo "Finding top polluted counties..."
	spark-submit scripts/batch_top_counties.py

batch-seasonal:
	@echo "Analyzing seasonal trends..."
	spark-submit scripts/batch_seasonal_trends.py

batch-yoy:
	@echo "Computing year-over-year changes..."
	spark-submit scripts/batch_yoy_comparison.py

batch-optimize:
	@echo "Running optimization experiments..."
	spark-submit --driver-memory 8g scripts/batch_optimization_comparison.py

batch-test:
	@echo "Running batch unit tests..."
	pytest tests/test_batch_transformations.py -v

batch-all: batch-state-agg batch-top-counties batch-seasonal batch-yoy
	@echo "✓ All batch jobs complete"

.PHONY: batch-state-agg batch-top-counties batch-seasonal batch-yoy batch-optimize batch-test batch-all

help-batch:
	@echo ""
	@echo "=========================================="
	@echo "Batch Processing Commands (Anshi's work)"
	@echo "=========================================="
	@echo ""
	@echo "  make batch-state-agg     - State-level monthly aggregations"
	@echo "  make batch-top-counties  - Top 10 polluted counties"
	@echo "  make batch-seasonal      - Seasonal PM2.5 trends"
	@echo "  make batch-yoy           - Year-over-year comparisons"
	@echo "  make batch-optimize      - Performance optimization tests"
	@echo "  make batch-test          - Run unit tests"
	@echo "  make batch-all           - Run all batch jobs"
	@echo ""
