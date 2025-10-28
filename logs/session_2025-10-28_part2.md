# Session 3: Spark Preprocessing Attempt

## Completed
- Tested Spark environment (3.5.3, 3 nodes)
- Sample conversion: 18.7M rows → 27.2 MB Parquet in 94s
- Compression ratio: ~85%

## Issue
- Full conversion too slow (10% in 35 min = 5+ hours total)
- Need optimization: more memory, better partitioning

## Next Session
- Optimize Spark config (more executors, adaptive execution)
- Process EPA separately from OpenAQ
- Target: <30 min for 289M rows
