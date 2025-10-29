from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, max as spark_max

spark = SparkSession.builder.appName("Analytics").getOrCreate()

epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")

print("=== TOP 5 STATES BY VIOLATION COUNT ===")
# EPA threshold: PM2.5 > 35, Ozone > 0.070
violations = epa.filter(
    ((col("Parameter Name") == "PM2.5 - Local Conditions") & (col("Sample Measurement") > 35)) |
    ((col("Parameter Name") == "Ozone") & (col("Sample Measurement") > 0.070))
)
violations.groupBy("State Name").count() \
    .orderBy(col("count").desc()).limit(5).show()

print("\n=== AVERAGE POLLUTANT LEVELS BY YEAR ===")
epa.filter(col("Parameter Name") == "PM2.5 - Local Conditions") \
    .groupBy("year_partition") \
    .agg(avg("Sample Measurement").alias("avg_pm25")) \
    .orderBy("year_partition").show()

spark.stop()
