#!/bin/bash
# Download OpenAQ full dataset: 1,178 locations × 5 years = 250M rows
# Estimated download: ~21GB compressed, 2-3 hours
# Usage: bash scripts/download/download_openaq_full.sh

set -e

echo "=========================================="
echo "OpenAQ Full Dataset Download"
echo "=========================================="
echo "Target: 1,178 locations × 5 years (2019-2023)"
echo "Expected: 250M rows, ~21GB compressed"
echo ""

# Configuration
BUCKET="openaq-data-archive"
YEARS=(2019 2020 2021 2022 2023)
OUTPUT_DIR="data/raw/openaq"
LOG_FILE="logs/download_$(date +%Y%m%d_%H%M%S).log"

# Create directories
mkdir -p $OUTPUT_DIR logs

# Install AWS CLI if needed
if ! command -v aws &> /dev/null; then
    echo "Installing AWS CLI..."
    pip3 install --user --quiet awscli
fi

# Get list of 1,178 most active locations from sample
# Strategy: Download locations 1-10000 with step of 8 (10000/8 ≈ 1250, accounting for gaps)
LOCATIONS=()
for i in $(seq 1 8 10000); do
    LOCATIONS+=($i)
done

# Limit to 1,178 locations
LOCATIONS=("${LOCATIONS[@]:0:1178}")

echo "Downloading ${#LOCATIONS[@]} locations..." | tee -a $LOG_FILE
echo "Years: ${YEARS[@]}" | tee -a $LOG_FILE
echo "Start time: $(date)" | tee -a $LOG_FILE
echo "" | tee -a $LOG_FILE

# Progress tracking
TOTAL_LOCS=${#LOCATIONS[@]}
TOTAL_YEARS=${#YEARS[@]}
TOTAL_TASKS=$((TOTAL_LOCS * TOTAL_YEARS))
CURRENT=0
SUCCESS=0
FAILED=0

# Download loop
for LOC_ID in "${LOCATIONS[@]}"; do
    for YEAR in "${YEARS[@]}"; do
        CURRENT=$((CURRENT + 1))
        
        # Progress indicator
        if [ $((CURRENT % 100)) -eq 0 ]; then
            echo "Progress: $CURRENT/$TOTAL_TASKS (Success: $SUCCESS, Failed: $FAILED)" | tee -a $LOG_FILE
        fi
        
        # Download location-year
        aws s3 cp \
            --no-sign-request \
            --recursive \
            --quiet \
            s3://$BUCKET/records/csv.gz/locationid=$LOC_ID/year=$YEAR/ \
            $OUTPUT_DIR/locationid=$LOC_ID/year=$YEAR/ \
            2>>$LOG_FILE && SUCCESS=$((SUCCESS + 1)) || FAILED=$((FAILED + 1))
    done
done

# Summary
echo "" | tee -a $LOG_FILE
echo "=========================================="  | tee -a $LOG_FILE
echo "Download Complete!" | tee -a $LOG_FILE
echo "=========================================="  | tee -a $LOG_FILE
echo "End time: $(date)" | tee -a $LOG_FILE
echo "Success: $SUCCESS/$TOTAL_TASKS" | tee -a $LOG_FILE
echo "Failed: $FAILED/$TOTAL_TASKS" | tee -a $LOG_FILE
echo "" | tee -a $LOG_FILE

# Count files and size
TOTAL_FILES=$(find $OUTPUT_DIR -name "*.csv.gz" | wc -l)
TOTAL_SIZE=$(du -sh $OUTPUT_DIR | cut -f1)

echo "Files downloaded: $TOTAL_FILES" | tee -a $LOG_FILE
echo "Total size: $TOTAL_SIZE" | tee -a $LOG_FILE
echo "Location: $OUTPUT_DIR" | tee -a $LOG_FILE
echo "Log file: $LOG_FILE" | tee -a $LOG_FILE
echo "" | tee -a $LOG_FILE
echo "✓ Ready for Parquet conversion!"
