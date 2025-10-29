import json

timing = {
    "Phase 1 - Data Ingestion": {
        "EPA download": "45 min",
        "OpenAQ download": "20 min", 
        "HDFS upload": "15 min",
        "Total rows": "289,283,534",
        "Storage": "51.7 GB CSV"
    },
    "Phase 2 - Preprocessing": {
        "Sample test": "94s for 18.7M rows",
        "Full conversion": "TBD",
        "Compression": "~85%"
    }
}

with open('/home/sd5957_nyu_edu/carbon_emissions/artifacts/timing_table.json', 'w') as f:
    json.dump(timing, f, indent=2)

print(json.dumps(timing, indent=2))
