from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import col
import time

spark = SparkSession.builder \
    .appName("Hyperparam_Tuning") \
    .config("spark.executor.memory", "16g") \
    .config("spark.executor.cores", "8") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

df = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/features_pm25")
df = df.select("Sample Measurement", "hour", "day_of_week", "month", 
               "Latitude", "Longitude", "rolling_avg_7d", "violation", "year_partition").dropna()

train = df.filter((col("year_partition") >= 2015) & (col("year_partition") <= 2020)).cache()
val = df.filter((col("year_partition") >= 2021) & (col("year_partition") <= 2022))

assembler = VectorAssembler(
    inputCols=["Sample Measurement", "hour", "day_of_week", "month", 
               "Latitude", "Longitude", "rolling_avg_7d"],
    outputCol="features"
)
train = assembler.transform(train)
val = assembler.transform(val)

evaluator = BinaryClassificationEvaluator(labelCol="violation")

# Test configurations
configs = [
    {"numTrees": 50, "maxDepth": 10, "name": "baseline"},
    {"numTrees": 100, "maxDepth": 12, "name": "more_trees_deeper"},
    {"numTrees": 75, "maxDepth": 15, "name": "deeper"},
    {"numTrees": 30, "maxDepth": 8, "name": "faster"}
]

results = []
for cfg in configs:
    start = time.time()
    rf = RandomForestClassifier(
        featuresCol="features", 
        labelCol="violation",
        numTrees=cfg["numTrees"],
        maxDepth=cfg["maxDepth"],
        seed=42
    )
    model = rf.fit(train)
    val_auc = evaluator.evaluate(model.transform(val))
    elapsed = time.time() - start
    
    print(f"\n{cfg['name']}: Trees={cfg['numTrees']}, Depth={cfg['maxDepth']}")
    print(f"Val AUC: {val_auc:.4f}, Time: {elapsed:.1f}s")
    results.append((cfg['name'], cfg['numTrees'], cfg['maxDepth'], val_auc, elapsed))

print("\n=== SUMMARY ===")
for r in results:
    print(f"{r[0]}: AUC={r[3]:.4f}, Time={r[4]:.1f}s")

spark.stop()
