# Batch Processing Optimization Results

## Query Performance Comparison
**Test:** Count PM2.5 records by state (66M rows)

| Strategy | Time | Speedup | Notes |
|----------|------|---------|-------|
| Baseline | 16.88s | 1.0x | Default Spark settings |
| Caching | 671.64s | 0.025x | Slower due to materialization overhead |
| Repartition(50) | 24.40s | 0.69x | Slight slowdown for single query |

## Key Findings
- **Caching hurts** on large datasets for single-use queries
- Baseline performs best for one-time aggregations
- Repartitioning useful only for repeated group-by on same column

## Batch Job Outputs
- `/batch/monthly_state_avg/` - 5,943 monthly aggregations
- `/batch/violations_by_state/` - 1,008 violation records
- `/batch/top_counties/` - Top 10 polluted counties
- `/batch/seasonal_trends/` - Seasonal PM2.5 by year
- `/batch/yoy_comparison/` - Year-over-year changes
- **Total size:** 626 KB
