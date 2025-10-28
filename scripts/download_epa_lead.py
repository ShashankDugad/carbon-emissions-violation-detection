import os
import requests
import zipfile
from datetime import datetime

BASE_URL = "https://aqs.epa.gov/aqsweb/airdata"

FILES = [
    'hourly_14129_2018.zip', 'hourly_14129_2019.zip', 'hourly_14129_2020.zip',
    'hourly_14129_2021.zip', 'hourly_14129_2022.zip', 'hourly_14129_2023.zip',
    'hourly_14129_2024.zip',  # Lead (Pb)
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

print("\nLead pollutant downloaded")
