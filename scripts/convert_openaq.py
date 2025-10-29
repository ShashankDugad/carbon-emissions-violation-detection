from pyspark.sql import SparkSession
from pyspark.sql.functions import year, to_timestamp, col, lit
import time

spark = SparkSession.builder \
    .appName("OpenAQ_Parquet") \
    .config("spark.executor.memory", "8g") \
    .getOrCreate()

start = time.time()

df = spark.read.csv("hdfs:///user/sd5957_nyu_edu/carbon_emissions/raw_data/openaq_combined.csv", header=True, inferSchema=True)
print(f"OpenAQ rows: {df.count():,}")

df = df.withColumn("year_partition", year(to_timestamp(col("datetime"))))

df.write.mode("overwrite") \
    .partitionBy("year_partition") \
    .parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/openaq_parquet")

elapsed = time.time() - start
print(f"Time: {elapsed:.1f}s")

spark.stop()
