import subprocess
import os

# Sample 250 high-quality locations from validated list
locations = list(range(2000, 2250))  # Active location IDs
years = [2023]  # Just 2023 for speed

TEMP_DIR = os.path.expanduser('~/carbon_emissions/temp/openaq')
os.makedirs(TEMP_DIR, exist_ok=True)

for loc in locations[:10]:  # Test with 10 first
    for year in years:
        cmd = f"aws s3 cp s3://openaq-data-archive/records/csv.gz/locationid={loc}/year={year}/ {TEMP_DIR}/loc_{loc}/ --recursive --no-sign-request --quiet"
        print(f"Downloading location {loc}, year {year}...")
        subprocess.run(cmd, shell=True)

print(f"\nOpenAQ sample downloaded to {TEMP_DIR}")
