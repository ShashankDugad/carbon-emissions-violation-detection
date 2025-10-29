from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, dayofweek, month, lag, avg as spark_avg
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("Feature_Engineering") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")

# Filter PM2.5 data only
pm25 = epa.filter(col("Parameter Name") == "PM2.5 - Local Conditions")

# Time features
pm25 = pm25.withColumn("hour", hour(col("Time Local"))) \
           .withColumn("day_of_week", dayofweek(col("Date Local"))) \
           .withColumn("month", month(col("Date Local")))

# Violation label (EPA threshold: 35)
pm25 = pm25.withColumn("violation", (col("Sample Measurement") > 35).cast("int"))

# Rolling averages (7-day window per site)
window = Window.partitionBy("State Code", "County Code", "Site Num") \
               .orderBy("Date Local").rowsBetween(-7, 0)
pm25 = pm25.withColumn("rolling_avg_7d", spark_avg("Sample Measurement").over(window))

# Save features
pm25.write.mode("overwrite") \
    .parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/features_pm25")

print(f"Features created: {pm25.count():,} rows")
print("Columns:", pm25.columns)

spark.stop()
