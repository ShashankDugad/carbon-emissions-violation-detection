| Phase | Input | Output | Time | Compression |
|-------|-------|--------|------|-------------|
| EPA Download | API | 43 GB CSV | 45 min | - |
| OpenAQ Download | S3 | 8.7 GB CSV | 20 min | - |
| EPA → Parquet | 43 GB | 311.5 MB | 4.6 min | 99.3% |
| OpenAQ → Parquet | 8.7 GB | 8.3 MB | 30 sec | 99.9% |
| **Total** | **51.7 GB** | **319.8 MB** | **70 min** | **99.4%** |
