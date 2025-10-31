# Hyperparameter Tuning Results

## Configurations Tested

| Config | Trees | Depth | Val AUC | Train Time |
|--------|-------|-------|---------|------------|
| Baseline | 50 | 10 | 0.9940 | 3.5 min |
| More trees | 100 | 12 | **0.9942** | 8.9 min |
| Deeper | 75 | 15 | 0.9941 | 9.4 min |
| Faster | 30 | 8 | 0.9938 | 1.9 min |

## Recommendation
**Use baseline (50 trees, depth 10)**
- Only 0.02% worse than best
- 2.5x faster training
- More practical for production
