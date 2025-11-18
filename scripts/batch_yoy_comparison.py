from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, lag
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("YoY_Comparison").getOrCreate()

epa = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")

yearly = epa.filter(col("Parameter Name") == "PM2.5 - Local Conditions") \
    .groupBy("year_partition") \
    .agg(avg("Sample Measurement").alias("avg_pm25"))

window = Window.orderBy("year_partition")
yoy = yearly.withColumn("prev_year_pm25", lag("avg_pm25").over(window)) \
    .withColumn("yoy_change", col("avg_pm25") - col("prev_year_pm25")) \
    .withColumn("yoy_pct", ((col("avg_pm25") - col("prev_year_pm25")) / col("prev_year_pm25") * 100))

yoy.write.mode("overwrite") \
    .parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/batch/yoy_comparison")

yoy.orderBy("year_partition").show(20, False)
spark.stop()
