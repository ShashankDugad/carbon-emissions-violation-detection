#!/bin/bash
# Download OpenAQ sample data (10 locations, 1 year for testing)
# Usage: bash scripts/download/download_openaq_sample.sh

set -e  # Exit on error

echo "=== OpenAQ Sample Download ==="
echo "Downloading 10 locations × 1 year (2023) for testing"
echo ""

# Configuration
BUCKET="openaq-data-archive"
YEAR=2023
OUTPUT_DIR="data/sample/openaq"
SAMPLE_LOCATIONS=(2178 1 10 100 1000 5000 10000 20000 50000 100000)

# Create output directory
mkdir -p $OUTPUT_DIR

# Download using AWS CLI (no credentials needed)
echo "Installing awscli if needed..."
pip3 install --user --quiet awscli

# Download each location
for LOC_ID in "${SAMPLE_LOCATIONS[@]}"; do
    echo "Downloading location $LOC_ID..."
    
    aws s3 cp \
        --no-sign-request \
        --recursive \
        s3://$BUCKET/records/csv.gz/locationid=$LOC_ID/year=$YEAR/ \
        $OUTPUT_DIR/locationid=$LOC_ID/year=$YEAR/ \
        2>/dev/null || echo "  Location $LOC_ID not found or empty, skipping..."
done

# Count downloaded files
TOTAL_FILES=$(find $OUTPUT_DIR -name "*.csv.gz" | wc -l)
TOTAL_SIZE=$(du -sh $OUTPUT_DIR | cut -f1)

echo ""
echo "✓ Download complete!"
echo "  Files: $TOTAL_FILES"
echo "  Size: $TOTAL_SIZE"
echo "  Location: $OUTPUT_DIR"
