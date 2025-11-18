from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, count
from pyspark.sql.types import StructType, DoubleType, StringType, IntegerType

spark = SparkSession.builder \
    .appName("Count_Violations") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3") \
    .getOrCreate()

schema = StructType() \
    .add("timestamp", StringType()) \
    .add("state", StringType()) \
    .add("pm25", DoubleType()) \
    .add("lat", DoubleType()) \
    .add("lon", DoubleType()) \
    .add("hour", IntegerType()) \
    .add("rolling_avg_7d", DoubleType())

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "air-quality") \
    .option("startingOffsets", "earliest") \
    .load()

parsed = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
violations = parsed.filter(col("pm25") > 35.0)

query = violations.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination(20)
spark.stop()
