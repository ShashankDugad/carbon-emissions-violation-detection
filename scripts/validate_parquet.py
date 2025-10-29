from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Validate_Parquet").getOrCreate()

df = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")

print(f"Total rows: {df.count():,}")
print(f"Partitions: {df.rdd.getNumPartitions()}")
print("\nSchema:")
df.printSchema()
print("\nNull counts:")
df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()

spark.stop()
