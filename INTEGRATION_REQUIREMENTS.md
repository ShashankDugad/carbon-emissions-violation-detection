# Team Integration Requirements

## For Anshi Shah (ans10020) - Batch Processing

### Input Data
- **Source:** `hdfs:///user/sd5957_nyu_edu/carbon_emissions/processed/epa_parquet/`
- **Rows:** 222M EPA records (2015-2024)
- **Schema:** 25 columns including State, County, PM2.5, Ozone, Date

### Required Deliverables
1. **State-level aggregations**
   - Monthly/yearly avg pollutant levels by state
   - Violation counts per state/year
   - Output: Parquet files in your HDFS path

2. **Cross-dataset joins** (if applicable)
   - Join EPA data with external datasets (weather, demographics, etc.)
   - Document join keys and methodology

3. **Batch analytics queries**
   - Top 10 most polluted counties
   - Seasonal trends analysis
   - Year-over-year comparisons

### Expected Outputs
- Location: `hdfs:///user/ans10020/batch_processed/`
- Format: Parquet (partitioned by year/state)
- Timing: Document processing time for performance comparison

### Integration Point
I will use your aggregated data for:
- Enhanced model features (state-level statistics)
- Comparative analysis (ML predictions vs batch analytics)
- Final report visualizations

---

## For Ronit Gehani (rg4881) - Streaming

### Input for Real-time Predictions
- **Model schema:** Use `features_pm25` Parquet for reference
- **Required features:**
```
  - Sample Measurement (current PM2.5)
  - hour, day_of_week, month
  - Latitude, Longitude
  - rolling_avg_7d (calculate from stream)
```

### Required Deliverables
1. **Streaming pipeline**
   - Kafka topic: Air quality sensor readings
   - Spark Structured Streaming consumer
   - Real-time violation detection (PM2.5 > 35)

2. **Model integration**
   - Load trained Random Forest model
   - Apply predictions on streaming data
   - Output: Violation alerts (timestamp, location, prediction)

3. **Performance metrics**
   - Throughput (records/second)
   - Latency (end-to-end processing time)
   - Accuracy on streaming data vs batch predictions

### Expected Outputs
- Stream output: Kafka topic or HDFS sink (`hdfs:///user/rg4881/streaming_output/`)
- Format: JSON or Parquet (micro-batches)
- Dashboard: Real-time violation map (optional)

### Model Artifact Needed
**I will provide:**
- Trained Random Forest model (serialized)
- Feature preprocessing pipeline
- Prediction threshold (currently 35 µg/m³)

**Location:** `hdfs:///user/sd5957_nyu_edu/carbon_emissions/models/rf_baseline.model`

### Integration Point
I will use your streaming results for:
- Real-time vs batch accuracy comparison
- Latency analysis (streaming predictions vs offline)
- Final demo: Live violation detection system

---

## Shared Coordination

### Timeline
- **By Nov 15:** Share initial outputs for integration testing
- **By Nov 25:** Final outputs with documentation
- **By Dec 5:** End-to-end integration complete

### Communication
- GitHub: https://github.com/ShashankDugad/carbon-emissions-violation-detection
- Shared HDFS paths: Document in README
- Issues/PRs for code review

### Quality Checklist
- [ ] Code committed to GitHub with clear README
- [ ] HDFS paths documented and accessible (chmod 755)
- [ ] Timing/performance metrics logged
- [ ] Sample outputs provided for testing
- [ ] Integration points identified

---

## Contact
**Shashank Dugad (sd5957) - Pipeline & ML**
- HDFS: `/user/sd5957_nyu_edu/carbon_emissions/`
- GitHub: https://github.com/ShashankDugad/carbon-emissions-violation-detection
- Data access: See TEAM_ACCESS.md
- ML artifacts: `/user/sd5957_nyu_edu/carbon_emissions/processed/`
