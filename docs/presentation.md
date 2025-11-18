# Carbon Emissions Violation Detection
**Big Data Final Project**

---

## Team
- **Shashank Dugad (sd5957)** - Pipeline & ML
- **Anshi Shah (ans10020)** - Batch Processing
- **Ronit Gehani (rg4881)** - Streaming & Production

---

## Problem Statement
**Challenge:** Predict EPA air quality violations (PM2.5 > 35 µg/m³)  
**Goal:** Enable early interventions to prevent health hazards  
**Scale:** 225M sensor readings (2015-2024)

---

## Data Pipeline

**Sources:**
- EPA AQS: 222M records (2015-2024)
- OpenAQ: 3M records (2023)
- Total: 51.7 GB CSV → 320 MB Parquet (99.4% compression)

**Processing:**
- HDFS storage with year partitioning
- Spark preprocessing (5 min for 225M rows)
- Feature engineering (66M PM2.5 records)

---

## Key Results

**ML Model:**
- Algorithm: Random Forest (50 trees, depth 10)
- Test AUC: **99.25%**
- Training time: 36 minutes
- Time-based split (2015-2020 train, 2023-2024 test)

**Feature Importance:**
- Current PM2.5: 52%
- 7-day rolling avg: 32%
- Combined: 84% predictive power

---

## Batch Analytics

**Top Findings:**
- California: 442K violations (72% of total)
- PM2.5 declined 12% (2015-2019)
- 2024: 18% drop vs 2023 spike

**Performance:**
- State aggregations: 5,943 monthly records
- Optimization: Baseline (16.88s) beats caching (671s)

---

## Streaming Pipeline

**Architecture:**
- Kafka 3.9.0 (3 partitions)
- Spark Structured Streaming
- Windowed aggregations (1-minute tumbling)
- Real-time violation detection

**Throughput:** 20 msgs/sec, <5s latency

---

## Technology Stack

- **Storage:** HDFS, Parquet
- **Processing:** Apache Spark 3.5.3
- **Streaming:** Kafka, Spark Structured Streaming
- **ML:** RandomForestClassifier
- **Visualization:** Streamlit, Plotly
- **Infrastructure:** NYU DataProc (3 nodes)

---

## Lessons Learned

**Successes:**
- Parquet compression (99.4%) enabled fast queries
- Time-based split prevented data leakage
- Feature engineering > complex models

**Challenges:**
- Kafka setup on shared cluster
- HDFS URI formatting
- Streaming checkpoint management

---

## Demo

**Live Dashboard:**
- Real-time metrics
- State-level violations
- PM2.5 trends (2015-2024)
- Streaming status

---

## Reproducibility

**One-command execution:**
```bash
make pipeline-full  # Full ML pipeline
make batch-all      # Batch processing
```

**GitHub:** All code, configs, tests
**CI/CD:** Automated linting & testing
**Documentation:** Architecture diagram, READMEs

---

## Future Work

- Deploy model as REST API
- Real-time alerting system
- Multi-pollutant prediction (Ozone, SO2)
- Integrate weather data
- Mobile app for public access

---

## Questions?

**GitHub:** github.com/ShashankDugad/carbon-emissions-violation-detection  
**Contact:** sd5957@nyu.edu

**Thank you!**
