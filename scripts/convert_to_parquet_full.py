from pyspark.sql import SparkSession
from pyspark.sql.functions import year, col, regexp_extract
import time

spark = SparkSession.builder \
    .appName("EPA_Full_Parquet") \
    .config("spark.executor.memory", "8g") \
    .config("spark.executor.cores", "4") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

start = time.time()

# Read all EPA files
epa_path = "hdfs:///user/sd5957_nyu_edu/carbon_emissions/raw_data/hourly_*.csv"
epa_df = spark.read.csv(epa_path, header=True, inferSchema=True)

# Read OpenAQ
openaq_df = spark.read.csv("hdfs:///user/sd5957_nyu_edu/carbon_emissions/raw_data/openaq_combined.csv", header=True, inferSchema=True)

print(f"EPA rows: {epa_df.count():,}")
print(f"OpenAQ rows: {openaq_df.count():,}")

# Add year partition and source
epa_df = epa_df.withColumn("year_partition", year(col("Date Local"))) \
               .withColumn("source", lit("EPA"))
               
openaq_df = openaq_df.withColumn("year_partition", year(col("datetime"))) \
                     .withColumn("source", lit("OpenAQ"))

# Union (align schemas later if needed)
df = epa_df.unionByName(openaq_df, allowMissingColumns=True)

# Write Parquet
df.write.mode("overwrite") \
    .partitionBy("year_partition", "source") \
    .parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/parquet")

elapsed = time.time() - start
print(f"Total time: {elapsed:.1f}s ({elapsed/60:.1f} min)")

spark.stop()
