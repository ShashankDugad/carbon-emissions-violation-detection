#!/usr/bin/env python3
"""
Validate OpenAQ sample data after download
Usage: python3 scripts/download/validate_openaq_sample.py
"""

import os
import gzip
import pandas as pd
from pathlib import Path

def validate_sample():
    """Validate downloaded OpenAQ sample data"""
    
    sample_dir = Path("data/sample/openaq")
    
    if not sample_dir.exists():
        print("❌ Sample directory not found!")
        return False
    
    # Find all CSV.GZ files
    csv_files = list(sample_dir.rglob("*.csv.gz"))
    
    if not csv_files:
        print("❌ No CSV.GZ files found!")
        return False
    
    print(f"✓ Found {len(csv_files)} compressed CSV files\n")
    
    # Validate first file
    print(f"Validating sample file: {csv_files[0].name}")
    
    try:
        with gzip.open(csv_files[0], 'rt') as f:
            df = pd.read_csv(f, nrows=10)
        
        print(f"  Rows (sample): {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        print(f"  Schema: {list(df.columns)}")
        print(f"\n  Sample data:")
        print(df.head(3))
        
        # Expected columns
        expected_cols = ['location_id', 'sensors_id', 'location', 'datetime', 
                        'lat', 'lon', 'parameter', 'units', 'value']
        
        missing_cols = set(expected_cols) - set(df.columns)
        if missing_cols:
            print(f"\n❌ Missing columns: {missing_cols}")
            return False
        
        print("\n✓ Schema validation passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

if __name__ == "__main__":
    success = validate_sample()
    exit(0 if success else 1)
