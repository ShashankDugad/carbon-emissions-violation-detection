from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, isnan

spark = SparkSession.builder.appName("Validate").getOrCreate()

# --- Try reading from HDFS, fallback to local data if unavailable ---
try:
    epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")
except Exception as e:
    print("⚠️ Could not load HDFS EPA data. Using local fallback at data/processed/epa_sample.parquet")
    epa = spark.read.parquet("data/processed/epa_sample.parquet")

print("=== EPA PARQUET ===")
print(f"Rows: {epa.count():,}")
print(f"Columns: {len(epa.columns)}")
print(f"Partitions: {epa.rdd.getNumPartitions()}")
print("\nSchema:")
epa.printSchema()
print("\nYear distribution:")
epa.groupBy("year_partition").count().orderBy("year_partition").show()

# --- Try OpenAQ parquet as well ---
try:
    openaq = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/openaq_parquet")
except Exception as e:
    print("⚠️ Could not load HDFS OpenAQ data. Using local fallback at data/processed/openaq_sample.parquet")
    openaq = spark.read.parquet("data/processed/openaq_sample.parquet")

print("\n=== OPENAQ PARQUET ===")
print(f"Rows: {openaq.count():,}")
print(f"Columns: {len(openaq.columns)}")

spark.stop()

# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, count, when, isnan

# spark = SparkSession.builder.appName("Validate").getOrCreate()

# # EPA
# epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")
# print("=== EPA PARQUET ===")
# print(f"Rows: {epa.count():,}")
# print(f"Columns: {len(epa.columns)}")
# print(f"Partitions: {epa.rdd.getNumPartitions()}")
# print("\nSchema:")
# epa.printSchema()
# print("\nYear distribution:")
# epa.groupBy("year_partition").count().orderBy("year_partition").show()

# # OpenAQ
# openaq = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/openaq_parquet")
# print("\n=== OPENAQ PARQUET ===")
# print(f"Rows: {openaq.count():,}")
# print(f"Columns: {len(openaq.columns)}")

# spark.stop()
