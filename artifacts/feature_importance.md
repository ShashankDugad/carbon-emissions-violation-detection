# Feature Importance Analysis

## Results (Random Forest, 30.6M training samples)

| Feature | Importance | Interpretation |
|---------|------------|----------------|
| Sample Measurement | 52.35% | Current PM2.5 level |
| Rolling 7-day avg | 32.06% | Recent trend |
| Longitude | 7.94% | East-West location |
| Month | 3.66% | Seasonal patterns |
| Latitude | 2.49% | North-South location |
| Hour | 1.19% | Time of day |
| Day of week | 0.31% | Weekly patterns |

**Key finding:** Current measurement + 7-day trend = 84% of predictive power
