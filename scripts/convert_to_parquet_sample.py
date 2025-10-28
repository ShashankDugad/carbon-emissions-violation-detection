from pyspark.sql import SparkSession
from pyspark.sql.functions import year, col
import time

spark = SparkSession.builder \
    .appName("EPA_Parquet_Sample") \
    .config("spark.executor.memory", "8g") \
    .config("spark.executor.cores", "4") \
    .config("spark.sql.shuffle.partitions", "100") \
    .getOrCreate()

start = time.time()

# Read sample EPA files (3 files = ~10% of data)
files = [
    "hdfs:///user/sd5957_nyu_edu/carbon_emissions/raw_data/hourly_44201_2024.csv",
    "hdfs:///user/sd5957_nyu_edu/carbon_emissions/raw_data/hourly_88101_2024.csv",
    "hdfs:///user/sd5957_nyu_edu/carbon_emissions/raw_data/hourly_42101_2024.csv"
]

df = spark.read.csv(files, header=True, inferSchema=True)
print(f"Sample rows: {df.count():,}")

# Add year partition column
df = df.withColumn("year_partition", year(col("Date Local")))

# Write as Parquet with partitioning
df.write.mode("overwrite") \
    .partitionBy("year_partition") \
    .parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/sample_parquet")

elapsed = time.time() - start
print(f"Time: {elapsed:.1f}s")

spark.stop()
