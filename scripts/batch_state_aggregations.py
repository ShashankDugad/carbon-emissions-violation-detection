from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, sum as spark_sum, year, month

spark = SparkSession.builder \
    .appName("Batch_State_Aggregations") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")

# Monthly avg by state
monthly = epa.filter(col("Parameter Name") == "PM2.5 - Local Conditions") \
    .groupBy("State Name", "year_partition", month("Date Local").alias("month")) \
    .agg(
        avg("Sample Measurement").alias("avg_pm25"),
        count("*").alias("measurement_count")
    )

monthly.write.mode("overwrite") \
    .partitionBy("year_partition", "State Name") \
    .parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/batch/monthly_state_avg")

# Violation counts by state/year
violations = epa.filter(
    ((col("Parameter Name") == "PM2.5 - Local Conditions") & (col("Sample Measurement") > 35)) |
    ((col("Parameter Name") == "Ozone") & (col("Sample Measurement") > 0.070))
).groupBy("State Name", "year_partition", "Parameter Name") \
 .agg(count("*").alias("violation_count"))

violations.write.mode("overwrite") \
    .partitionBy("year_partition") \
    .parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/batch/violations_by_state")

print(f"Monthly aggregations: {monthly.count():,} rows")
print(f"Violation counts: {violations.count():,} rows")

spark.stop()
