#!/usr/bin/env python3
"""
Convert OpenAQ CSV.GZ to Parquet - No Slurm needed
Usage: python3 src/preprocessing/convert_to_parquet.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, year, month
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Config
INPUT = "data/raw/openaq/**/**.csv.gz"
OUTPUT = "data/processed/openaq_parquet"

# Create Spark
spark = SparkSession.builder \
    .appName("OpenAQ-Convert") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

logger.info("Reading CSV.GZ files...")
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(INPUT)

# Add partitions
df = df.withColumn("year", year(col("datetime"))) \
       .withColumn("month", month(col("datetime")))

logger.info(f"Rows: {df.count():,}")

logger.info("Writing Parquet...")
df.write.mode("overwrite").partitionBy("year", "parameter").parquet(OUTPUT, compression="snappy")

logger.info("✓ Done!")
spark.stop()
