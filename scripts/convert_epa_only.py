from pyspark.sql import SparkSession
from pyspark.sql.functions import year, col
import time

spark = SparkSession.builder \
    .appName("EPA_Only_Parquet") \
    .config("spark.executor.memory", "12g") \
    .config("spark.executor.cores", "8") \
    .config("spark.executor.instances", "3") \
    .config("spark.sql.shuffle.partitions", "300") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

start = time.time()

epa_path = "hdfs:///user/sd5957_nyu_edu/carbon_emissions/raw_data/hourly_*.csv"
df = spark.read.csv(epa_path, header=True, inferSchema=True)

print(f"EPA rows: {df.count():,}")

df = df.withColumn("year_partition", year(col("Date Local")))

df.write.mode("overwrite") \
    .partitionBy("year_partition") \
    .parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")

elapsed = time.time() - start
print(f"Time: {elapsed:.1f}s ({elapsed/60:.1f} min)")

spark.stop()
