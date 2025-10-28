import os
import requests
import zipfile
from datetime import datetime

BASE_URL = "https://aqs.epa.gov/aqsweb/airdata"

# Additional pollutants to reach 200M+
FILES = [
    'hourly_42401_2018.zip', 'hourly_42401_2019.zip', 'hourly_42401_2020.zip',
    'hourly_42401_2021.zip', 'hourly_42401_2022.zip', 'hourly_42401_2023.zip',
    'hourly_42401_2024.zip',  # SO2
    'hourly_42101_2018.zip', 'hourly_42101_2019.zip', 'hourly_42101_2020.zip',
    'hourly_42101_2021.zip', 'hourly_42101_2022.zip', 'hourly_42101_2023.zip',
    'hourly_42101_2024.zip',  # CO
    'hourly_42602_2018.zip', 'hourly_42602_2019.zip', 'hourly_42602_2020.zip',
    'hourly_42602_2021.zip', 'hourly_42602_2022.zip', 'hourly_42602_2023.zip',
    'hourly_42602_2024.zip',  # NO2
]

TEMP_DIR = os.path.expanduser('~/carbon_emissions/temp')
os.makedirs(TEMP_DIR, exist_ok=True)

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

print("\nAll additional pollutants downloaded to ~/carbon_emissions/temp/")
