import subprocess
import os

# 250 locations for ~50M rows
locations = list(range(2000, 2250))
years = [2023]

TEMP_DIR = os.path.expanduser('~/carbon_emissions/temp/openaq')
os.makedirs(TEMP_DIR, exist_ok=True)

total = len(locations) * len(years)
count = 0

for loc in locations:
    for year in years:
        count += 1
        cmd = f"aws s3 cp s3://openaq-data-archive/records/csv.gz/locationid={loc}/year={year}/ {TEMP_DIR}/loc_{loc}/ --recursive --no-sign-request --quiet"
        print(f"[{count}/{total}] Location {loc}, {year}...", end=' ', flush=True)
        result = subprocess.run(cmd, shell=True, capture_output=True)
        if result.returncode == 0:
            print("✓")
        else:
            print("✗")

print(f"\nDownload complete")
