import os
import requests
import zipfile
from datetime import datetime

BASE_URL = "https://aqs.epa.gov/aqsweb/airdata"

# Extend to 2015-2017 for Ozone and PM2.5
FILES = [
    'hourly_44201_2015.zip', 'hourly_44201_2016.zip', 'hourly_44201_2017.zip',  # Ozone
    'hourly_88101_2015.zip', 'hourly_88101_2016.zip', 'hourly_88101_2017.zip',  # PM2.5
]

TEMP_DIR = os.path.expanduser('~/carbon_emissions/temp')

for file in FILES:
    url = f"{BASE_URL}/{file}"
    zip_path = f"{TEMP_DIR}/{file}"
    
    print(f"Downloading {file}...", end=' ', flush=True)
    start = datetime.now()
    
    response = requests.get(url, stream=True, timeout=600)
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)
    
    print(f"Extracting...", end=' ', flush=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(TEMP_DIR)
    
    os.remove(zip_path)
    elapsed = (datetime.now() - start).total_seconds()
    print(f"Done ({elapsed:.1f}s)")

print("\n2015-2017 data downloaded")
