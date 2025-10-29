from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, isnan

spark = SparkSession.builder.appName("Validate").getOrCreate()

# EPA
epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")
print("=== EPA PARQUET ===")
print(f"Rows: {epa.count():,}")
print(f"Columns: {len(epa.columns)}")
print(f"Partitions: {epa.rdd.getNumPartitions()}")
print("\nSchema:")
epa.printSchema()
print("\nYear distribution:")
epa.groupBy("year_partition").count().orderBy("year_partition").show()

# OpenAQ
openaq = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/openaq_parquet")
print("\n=== OPENAQ PARQUET ===")
print(f"Rows: {openaq.count():,}")
print(f"Columns: {len(openaq.columns)}")

spark.stop()
