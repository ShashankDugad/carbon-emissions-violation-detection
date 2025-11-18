from kafka import KafkaProducer
import pandas as pd
import json
import time

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Load pre-sampled data
import subprocess
subprocess.run(['hdfs', 'dfs', '-get', 
                'hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/features_pm25/', 
                '/tmp/features_sample/'], check=False)

# Read parquet files
import pyarrow.parquet as pq
table = pq.read_table('/tmp/features_sample')
df = table.to_pandas().sample(660, random_state=42)

print(f"Sending {len(df)} records to Kafka...")

for idx, row in df.iterrows():
    message = {
        'timestamp': str(row['Date Local']),
        'state': row['State Name'],
        'pm25': float(row['Sample Measurement']),
        'lat': float(row['Latitude']),
        'lon': float(row['Longitude']),
        'hour': int(row['hour']),
        'rolling_avg_7d': float(row['rolling_avg_7d']) if pd.notna(row['rolling_avg_7d']) else 0.0
    }
    producer.send('air-quality', value=message)
    time.sleep(0.1)
    
    if idx % 100 == 0:
        print(f"Sent {idx} records")

producer.flush()
print("Complete")
