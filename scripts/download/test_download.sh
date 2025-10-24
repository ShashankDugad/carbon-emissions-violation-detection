#!/bin/bash
set -e
echo "Testing OpenAQ download with 2 locations..."
BUCKET="openaq-data-archive"
YEAR=2023
OUTPUT_DIR="data/sample/openaq_test"
mkdir -p $OUTPUT_DIR

pip3 install --user --quiet awscli

echo "Downloading location 2178 (known good)..."
aws s3 cp --no-sign-request --recursive \
    s3://$BUCKET/records/csv.gz/locationid=2178/year=$YEAR/ \
    $OUTPUT_DIR/locationid=2178/year=$YEAR/ \
    || echo "Failed"

ls -lh $OUTPUT_DIR/locationid=2178/year=$YEAR/ | head -5
