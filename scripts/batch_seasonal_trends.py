from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, month, when

spark = SparkSession.builder.appName("Seasonal_Trends").getOrCreate()

epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")

# Add month column first
seasonal = epa.filter(col("Parameter Name") == "PM2.5 - Local Conditions") \
    .withColumn("month", month("Date Local")) \
    .withColumn("season", 
        when(col("month").isin(12,1,2), "Winter")
        .when(col("month").isin(3,4,5), "Spring")
        .when(col("month").isin(6,7,8), "Summer")
        .otherwise("Fall")
    ) \
    .groupBy("year_partition", "season") \
    .agg(avg("Sample Measurement").alias("avg_pm25"))

seasonal.write.mode("overwrite") \
    .partitionBy("year_partition") \
    .parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/batch/seasonal_trends")

seasonal.orderBy("year_partition", "season").show(40, False)
spark.stop()
