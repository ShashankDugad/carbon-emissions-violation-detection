from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

spark = SparkSession.builder.appName("Top_Counties").getOrCreate()

epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")

# Top 10 counties by avg PM2.5
top_counties = epa.filter(col("Parameter Name") == "PM2.5 - Local Conditions") \
    .groupBy("State Name", "County Name") \
    .agg(
        avg("Sample Measurement").alias("avg_pm25"),
        count("*").alias("sample_count")
    ) \
    .filter(col("sample_count") > 1000) \
    .orderBy(col("avg_pm25").desc()) \
    .limit(10)

top_counties.write.mode("overwrite") \
    .parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/batch/top_counties")

top_counties.show(10, False)
spark.stop()
