from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, count
from pyspark.sql.types import StructType, DoubleType, StringType, IntegerType, TimestampType

spark = SparkSession.builder \
    .appName("Streaming_Windowed") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3") \
    .getOrCreate()

schema = StructType() \
    .add("timestamp", TimestampType()) \
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

# 1-minute tumbling window aggregations
windowed = parsed.groupBy(
    window(col("timestamp"), "1 minute"),
    col("state")
).agg(
    avg("pm25").alias("avg_pm25"),
    count("*").alias("record_count")
)

query = windowed.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination(30)
