# Team Data Access Guide

## Parquet Files (HDFS)

### EPA Data (222M rows, 311 MB)
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("TeamAccess").getOrCreate()
epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")
```

### OpenAQ Data (3M rows, 8 MB)
```python
openaq = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/openaq_parquet")
```

### ML Features (66M PM2.5 records, 239 MB)
```python
features = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/features_pm25")
```

## Integration Points

### For Batch Processing (Anshi)
- Input: `epa_parquet/` and `openaq_parquet/`
- Suggested tasks: Aggregations by state/year, join with external datasets
- Output: Save to your own HDFS path

### For Streaming (Ronit)
- Schema reference: Use `features_pm25` for consistent schema
- Real-time predictions: Load trained model, apply to streaming data
- Suggested: Kafka → Spark Streaming → violation alerts

## Quick Tests
```bash
# Count rows
spark-submit --driver-memory 4g << 'PYEOF'
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Test").getOrCreate()
epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")
print(f"EPA rows: {epa.count():,}")
spark.stop()
PYEOF
```
