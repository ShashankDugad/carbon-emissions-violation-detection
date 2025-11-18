from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

states = ['California', 'Texas', 'New York', 'Florida', 'Illinois']
print("Sending 500 simulated records...")

for i in range(500):
    message = {
        'timestamp': f'2024-11-{random.randint(1,30):02d} {random.randint(0,23):02d}:00:00',
        'state': random.choice(states),
        'pm25': random.uniform(5, 50),
        'lat': random.uniform(25, 48),
        'lon': random.uniform(-120, -70),
        'hour': random.randint(0, 23),
        'rolling_avg_7d': random.uniform(5, 40)
    }
    producer.send('air-quality', value=message)
    
    if i % 100 == 0:
        print(f"Sent {i}")
        
    time.sleep(0.05)  # 20/sec

producer.flush()
print("Done")
