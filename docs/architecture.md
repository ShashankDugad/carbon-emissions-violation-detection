# System Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                             │
├──────────────────────┬──────────────────────────────────────────┤
│  EPA AQS API         │  OpenAQ S3 Bucket                        │
│  (286M records)      │  (3M records)                            │
└──────────┬───────────┴────────────┬─────────────────────────────┘
           │                        │
           ▼                        ▼
    ┌──────────────────────────────────────┐
    │      DATA INGESTION LAYER            │
    │  • Python download scripts           │
    │  • CSV format (51.7 GB)              │
    └──────────────┬───────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │   HDFS STORAGE      │
         │  /raw_data/         │
         └──────────┬──────────┘
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │     SPARK PREPROCESSING               │
    │  • CSV → Parquet conversion           │
    │  • Partitioning by year               │
    │  • Compression: 99.4%                 │
    │  • Output: 319.8 MB                   │
    └──────────┬────────────────────────────┘
               │
               ├──────────────────┬────────────────────┐
               ▼                  ▼                    ▼
    ┌──────────────────┐  ┌──────────────┐  ┌─────────────────┐
    │  EPA Parquet     │  │OpenAQ Parquet│  │ Features (PM2.5)│
    │  (311.5 MB)      │  │  (8.3 MB)    │  │   (239 MB)      │
    └──────┬───────────┘  └──────┬───────┘  └────────┬────────┘
           │                     │                    │
           └─────────────────────┴────────────────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           ▼                     ▼                     ▼
    ┌─────────────┐    ┌──────────────────┐   ┌─────────────────┐
    │   BATCH     │    │   STREAMING      │   │   ML MODEL      │
    │ PROCESSING  │    │   PIPELINE       │   │   TRAINING      │
    │             │    │                  │   │                 │
    │ • State agg │    │ • Kafka broker   │   │ • Random Forest │
    │ • Trends    │    │ • Spark Stream   │   │ • 99.25% AUC    │
    │ • Top-k     │    │ • Windowed agg   │   │ • Time-split    │
    └─────┬───────┘    └────────┬─────────┘   └────────┬────────┘
          │                     │                       │
          └─────────────────────┴───────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   VISUALIZATION       │
                    │  • Streamlit Dashboard│
                    │  • Plotly Charts      │
                    │  • Real-time Metrics  │
                    └───────────────────────┘
```

## Technology Stack
- Storage: HDFS, Parquet
- Processing: Apache Spark 3.5.3
- Streaming: Kafka 3.9.0
- ML: RandomForestClassifier (99.25% AUC)
- Visualization: Streamlit, Plotly
- Infrastructure: NYU DataProc (3 nodes)
