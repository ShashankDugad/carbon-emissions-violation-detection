from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("Feature_Importance_Optimized") \
    .config("spark.executor.memory", "16g") \
    .config("spark.executor.cores", "8") \
    .config("spark.executor.instances", "3") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.default.parallelism", "24") \
    .getOrCreate()

df = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/features_pm25")
df = df.select("Sample Measurement", "hour", "day_of_week", "month", 
               "Latitude", "Longitude", "rolling_avg_7d", "violation", "year_partition").dropna()

# Cache filtered data
train = df.filter((col("year_partition") >= 2015) & (col("year_partition") <= 2020)).cache()

feature_cols = ["Sample Measurement", "hour", "day_of_week", "month", 
                "Latitude", "Longitude", "rolling_avg_7d"]
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
train = assembler.transform(train)

rf = RandomForestClassifier(featuresCol="features", labelCol="violation", 
                            numTrees=50, maxDepth=10, seed=42)
model = rf.fit(train)

importances = model.featureImportances.toArray()
print(f"\nTrain: {train.count():,} rows")
print("\n=== FEATURE IMPORTANCE ===")
for i, feat in enumerate(feature_cols):
    print(f"{feat}: {importances[i]:.4f}")

spark.stop()
