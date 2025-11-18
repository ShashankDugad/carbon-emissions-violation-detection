import pytest
import subprocess

def test_batch_pipeline():
    """Test batch processing outputs exist"""
    result = subprocess.run(
        ['hdfs', 'dfs', '-test', '-d', '/user/sd5957_nyu_edu/carbon_emissions/batch/monthly_state_avg'],
        capture_output=True
    )
    assert result.returncode == 0, "Monthly aggregations missing"

def test_parquet_output():
    """Test Parquet files exist"""
    result = subprocess.run(
        ['hdfs', 'dfs', '-test', '-d', '/user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet'],
        capture_output=True
    )
    assert result.returncode == 0, "EPA Parquet missing"

def test_kafka_topic():
    """Test Kafka topic exists"""
    result = subprocess.run(
        ['/home/sd5957_nyu_edu/kafka_2.13-3.9.0/bin/kafka-topics.sh', '--list', '--bootstrap-server', 'localhost:9092'],
        capture_output=True, text=True
    )
    assert 'air-quality' in result.stdout, "Kafka topic missing"

def test_makefile_targets():
    """Test Makefile has required targets"""
    with open('Makefile', 'r') as f:
        content = f.read()
    assert 'batch-all' in content
    assert 'pipeline-train' in content
