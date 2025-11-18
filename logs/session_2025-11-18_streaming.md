# Session 11: Streaming Setup (Ronit's Work - Partial)

## Completed
1. ✓ Kafka installed (3.9.0) on custom port 2182
2. ✓ Topic created: air-quality (3 partitions)
3. ✓ Producer: 500 simulated records sent
4. ✓ Spark Streaming consumer: Reads from Kafka
5. ✓ Violations filter: pm25 > 35

## Issues
- HDFS write failed (URI authority error)
- Console output showed no violations (timing issue)

## Next Steps
- Fix HDFS streaming sink
- Add windowed aggregations
- Dashboard creation
- Integration tests
