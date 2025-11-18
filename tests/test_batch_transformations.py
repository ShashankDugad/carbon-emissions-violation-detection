import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.appName("Tests").getOrCreate()

def test_state_aggregation(spark):
    """Test state-level PM2.5 aggregation"""
    df = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")
    result = df.filter(col("Parameter Name") == "PM2.5 - Local Conditions") \
        .groupBy("State Name").agg(avg("Sample Measurement").alias("avg_pm25"))
    
    assert result.count() > 0, "No states found"
    assert result.filter(col("avg_pm25") < 0).count() == 0, "Negative PM2.5 values"

def test_violation_detection(spark):
    """Test violation threshold logic"""
    df = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet")
    violations = df.filter(
        (col("Parameter Name") == "PM2.5 - Local Conditions") & (col("Sample Measurement") > 35)
    )
    
    assert violations.count() > 0, "No violations detected"
    assert violations.filter(col("Sample Measurement") <= 35).count() == 0, "Invalid violations"

def test_seasonal_assignment(spark):
    """Test season categorization"""
    from pyspark.sql.functions import month, when
    
    df = spark.read.parquet("hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet").limit(1000)
    df = df.withColumn("month", month("Date Local")) \
        .withColumn("season", 
            when(col("month").isin(12,1,2), "Winter")
            .when(col("month").isin(3,4,5), "Spring")
            .when(col("month").isin(6,7,8), "Summer")
            .otherwise("Fall")
        )
    
    assert df.filter(col("season").isNull()).count() == 0, "Null seasons found"
