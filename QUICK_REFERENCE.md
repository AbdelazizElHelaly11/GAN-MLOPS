# Quick Reference - Pipeline Testing

## Generate Screenshots

### 1️⃣ Failed Run (Accuracy < 85%)
```
1. Go to GitHub → Actions tab
2. Select "ML Model Validation and Deployment Pipeline"
3. Click "Run workflow"
4. Set epochs = 1
5. Run and wait
6. Screenshot: Deploy job with RED X (failed)
```

### 2️⃣ Successful Run (Accuracy > 85%)
```
1. Go to GitHub → Actions tab
2. Select "ML Model Validation and Deployment Pipeline"
3. Click "Run workflow"
4. Set epochs = 10 (or default)
5. Run and wait
6. Screenshot: Both jobs with GREEN ✓ (passed)
```

## Git Commands to Push

```bash
cd "C:\Users\hzezo\OneDrive\Desktop\gan_project"

# Add all files
git add .

# Commit
git commit -m "feat: implement multi-job ML pipeline with threshold validation"

# Push
git push origin ci-test
```

## Files to Submit

1. ✅ `.github/workflows/pipeline.yml` (the main YAML)
2. 📸 Screenshot of FAILED run
3. 📸 Screenshot of SUCCESSFUL run

## What Each File Does

| File | Purpose |
|------|---------|
| `train.py` | Trains MNIST classifier, logs to MLflow, exports Run ID |
| `check_threshold.py` | Checks if accuracy ≥ 85% |
| `pipeline.yml` | GitHub Actions workflow (2 jobs) |
| `Dockerfile` | Container with RUN_ID arg |
| `data.dvc` | DVC data tracking |

## Key Points

- **Low accuracy**: Use EPOCHS=1 → ~70% accuracy → FAIL
- **High accuracy**: Use EPOCHS=10 → ~97% accuracy → PASS
- **Threshold**: 0.85 (85%)
- **Artifact**: model_info.txt contains MLflow Run ID
