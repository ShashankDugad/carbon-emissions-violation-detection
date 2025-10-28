import requests
import gzip
import os
from datetime import datetime

BASE_URL = "https://www.ncei.noaa.gov/data/global-hourly/access"
TEMP_DIR = os.path.expanduser('~/carbon_emissions/temp/noaa')
os.makedirs(TEMP_DIR, exist_ok=True)

# Major US station IDs (USAF-WBAN format)
STATIONS = {
    '722190-13874': 'ATL', '722598-03927': 'DFW', '725650-00240': 'DEN',
    '725300-94846': 'ORD', '722950-23174': 'LAX', '723140-03812': 'CLT',
    '723860-23169': 'LAS', '722780-23183': 'PHX', '722050-12815': 'MCO',
    '727930-24233': 'SEA', '725020-14734': 'EWR', '724940-23234': 'SFO',
    '722430-12960': 'IAH', '725090-14739': 'BOS', '726580-14922': 'MSP',
    '725370-94847': 'DTW', '724080-13739': 'PHL', '725030-14732': 'LGA',
    '724060-93721': 'BWI', '725720-24127': 'SLC', '724050-13743': 'DCA'
}

YEARS = range(2018, 2025)
success = 0

for station_id, code in STATIONS.items():
    for year in YEARS:
        filename = f"{station_id}.csv"
        url = f"{BASE_URL}/{year}/{filename}"
        output = f"{TEMP_DIR}/{code}_{year}.csv"
        
        try:
            print(f"{code}_{year}...", end=' ', flush=True)
            resp = requests.get(url, timeout=30)
            
            if resp.status_code == 200:
                with open(output, 'wb') as f:
                    f.write(resp.content)
                success += 1
                print("✓")
            else:
                print(f"✗ {resp.status_code}")
        except Exception as e:
            print(f"✗")

print(f"\nSuccess: {success} files")
