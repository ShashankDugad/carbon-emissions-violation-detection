from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, avg, count, when
import time
from datetime import datetime

# Spark session (local mode for testing)
spark = (
    SparkSession.builder
    .appName("BatchStateAnalytics")
    .master("local[*]")  # Use all local cores
    .getOrCreate()
)

start = time.time()

# === Load Data ===
# These HDFS paths are placeholders for later DataProc runs
epa_path = "hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet/"
openaq_path = "hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/openaq_parquet/"

print(f"Starting batch analytics at {datetime.now()}")

try:
    epa_df = spark.read.parquet(epa_path)
    openaq_df = spark.read.parquet(openaq_path)
    print("✅ Data loaded successfully")
except Exception as e:
    print("⚠️ Could not load HDFS data (running locally?). Using sample schema instead.")
    from pyspark.sql import Row
    sample = [
        Row(State="CA", Date="2024-06-01", PM25=40.2, Ozone=0.03),
        Row(State="NY", Date="2024-06-01", PM25=28.7, Ozone=0.02),
        Row(State="TX", Date="2024-06-01", PM25=35.9, Ozone=0.05)
    ]
    df = spark.createDataFrame(sample)
else:
    df = epa_df.unionByName(openaq_df, allowMissingColumns=True)

# === Feature Engineering ===
df = df.withColumn("year", year(col("Date"))).withColumn("month", month(col("Date")))

# === Aggregations ===
state_monthly = (
    df.groupBy("State", "year", "month")
      .agg(
          avg("PM25").alias("avg_pm25"),
          avg("Ozone").alias("avg_ozone"),
          count(when(col("PM25") > 35, True)).alias("violation_count")
      )
)

# === Save Output (local or later HDFS) ===
output_path = "outputs/state_aggregates_test/"  # temporary local output
state_monthly.write.mode("overwrite").parquet(output_path)

end = time.time()
duration = (end - start) / 60

# === Log Summary ===
log_text = f"""
# Batch Analytics Run — {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- Status: ✅ Completed
- Output Path: {output_path}
- Processing Time: {duration:.2f} minutes
- Records: {state_monthly.count()}
"""

with open("logs/session_batch_analytics.md", "a") as f:
    f.write(log_text + "\n")

print("✅ Batch processing complete.")
print(log_text)

spark.stop()
