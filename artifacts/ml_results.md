# ML Baseline Results

## Model: Random Forest (50 trees, depth 10)

## Time-based Split
- Train: 2015-2020 (30.6M rows)
- Val: 2021-2022 (18.1M rows)  
- Test: 2023-2024 (17.4M rows)

## Performance
- Validation AUC: 0.9937
- Test AUC: 0.9925
- Training time: 36 min

## Features
- PM2.5 measurement
- Time: hour, day_of_week, month
- Location: lat/long
- Rolling 7-day average
