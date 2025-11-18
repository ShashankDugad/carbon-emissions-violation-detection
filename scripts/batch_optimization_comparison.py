from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count
import time

spark = SparkSession.builder.appName("Optimization_Test").getOrCreate()

epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")

# Test 1: No optimization
start = time.time()
result1 = epa.filter(col("Parameter Name") == "PM2.5 - Local Conditions") \
    .groupBy("State Name").agg(count("*").alias("count")).collect()
time1 = time.time() - start

# Test 2: With caching
epa_cached = epa.cache()
start = time.time()
result2 = epa_cached.filter(col("Parameter Name") == "PM2.5 - Local Conditions") \
    .groupBy("State Name").agg(count("*").alias("count")).collect()
time2 = time.time() - start

# Test 3: Repartition
epa_repart = epa.repartition(50, "State Name")
start = time.time()
result3 = epa_repart.filter(col("Parameter Name") == "PM2.5 - Local Conditions") \
    .groupBy("State Name").agg(count("*").alias("count")).collect()
time3 = time.time() - start

print(f"\n=== OPTIMIZATION RESULTS ===")
print(f"No optimization: {time1:.2f}s")
print(f"With caching: {time2:.2f}s")
print(f"Repartitioned: {time3:.2f}s")

spark.stop()
