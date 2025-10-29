from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import time
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("ML_TimeSplit").getOrCreate()

start = time.time()
df = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/features_pm25")
df = df.select("Sample Measurement", "hour", "day_of_week", "month", 
               "Latitude", "Longitude", "rolling_avg_7d", "violation", "year_partition").dropna()

# Time-based split
train = df.filter((col("year_partition") >= 2015) & (col("year_partition") <= 2020))
val = df.filter((col("year_partition") >= 2021) & (col("year_partition") <= 2022))
test = df.filter((col("year_partition") >= 2023) & (col("year_partition") <= 2024))

assembler = VectorAssembler(
    inputCols=["Sample Measurement", "hour", "day_of_week", "month", 
               "Latitude", "Longitude", "rolling_avg_7d"],
    outputCol="features"
)
train = assembler.transform(train)
val = assembler.transform(val)
test = assembler.transform(test)

rf = RandomForestClassifier(featuresCol="features", labelCol="violation", 
                            numTrees=50, maxDepth=10)
model = rf.fit(train)

evaluator = BinaryClassificationEvaluator(labelCol="violation")
val_auc = evaluator.evaluate(model.transform(val))
test_auc = evaluator.evaluate(model.transform(test))

elapsed = time.time() - start
print(f"Train: 2015-2020, {train.count():,} rows")
print(f"Val: 2021-2022, {val.count():,} rows")
print(f"Test: 2023-2024, {test.count():,} rows")
print(f"Val AUC: {val_auc:.4f}")
print(f"Test AUC: {test_auc:.4f}")
print(f"Time: {elapsed:.1f}s")

spark.stop()
