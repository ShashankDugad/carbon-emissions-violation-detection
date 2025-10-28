from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Carbon_Emissions_Test") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "4") \
    .getOrCreate()

print(f"Spark Version: {spark.version}")
print(f"Executors: {spark.sparkContext.defaultParallelism}")

# Test HDFS read
df = spark.read.csv("hdfs:///user/sd5957_nyu_edu/carbon_emissions/raw_data/hourly_44201_2024.csv", header=True, inferSchema=True)
print(f"Test file rows: {df.count()}")
print("Schema:")
df.printSchema()

spark.stop()
