import os
import requests
import gzip
import shutil
from datetime import datetime

BASE_URL = "https://www.ncei.noaa.gov/data/local-climatological-data/access"
TEMP_DIR = os.path.expanduser('~/carbon_emissions/temp/noaa')
os.makedirs(TEMP_DIR, exist_ok=True)

# Major US stations (100 busiest airports with weather data)
STATIONS = [
    'ATL', 'DFW', 'DEN', 'ORD', 'LAX', 'CLT', 'LAS', 'PHX', 'MCO', 'SEA',
    'EWR', 'SFO', 'IAH', 'BOS', 'MSP', 'DTW', 'PHL', 'LGA', 'BWI', 'SLC',
    'DCA', 'MDW', 'SAN', 'TPA', 'PDX', 'HOU', 'STL', 'RDU', 'AUS', 'BNA',
    'OAK', 'MCI', 'SNA', 'MSY', 'SAT', 'SMF', 'PIT', 'CLE', 'IND', 'CMH',
    'MKE', 'OMA', 'RIC', 'BUF', 'OKC', 'MEM', 'TUS', 'ABQ', 'BDL', 'BUR'
]

YEARS = range(2018, 2025)

total_files = 0
for year in YEARS:
    for station in STATIONS:
        filename = f"{station}_{year}.csv"
        url = f"{BASE_URL}/{year}/{filename}"
        output_path = f"{TEMP_DIR}/{filename}"
        
        try:
            print(f"{filename}...", end=' ', flush=True)
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                total_files += 1
                print("✓")
            else:
                print(f"✗ {response.status_code}")
        except Exception as e:
            print(f"✗ {str(e)[:30]}")

print(f"\nDownloaded {total_files} NOAA files to {TEMP_DIR}")
