# ML Pipeline Assignment - Testing Guide

## Overview
This pipeline trains an MNIST classifier and deploys it only if accuracy ≥ 85%.

## Components
1. **train.py** - Trains MNIST classifier, logs to MLflow, exports run ID
2. **check_threshold.py** - Validates accuracy threshold
3. **Dockerfile** - Container with RUN_ID argument for model deployment
4. **pipeline.yml** - Two-job GitHub Actions workflow

## Local Testing

### Test 1: Successful Run (Accuracy > 85%)
```bash
# Train with enough epochs for high accuracy
cd "C:\Users\hzezo\OneDrive\Desktop\gan_project"
$env:EPOCHS="10"
python train.py

# Check threshold
python check_threshold.py
```

### Test 2: Failed Run (Accuracy < 85%)
```bash
# Train with very few epochs for low accuracy
cd "C:\Users\hzezo\OneDrive\Desktop\gan_project"
$env:EPOCHS="1"
python train.py

# Check threshold (should fail)
python check_threshold.py
```

## GitHub Actions Testing

### Trigger Successful Run
```bash
# Push to trigger with default 10 epochs
git add .
git commit -m "Test: successful pipeline run"
git push
```

### Trigger Failed Run
Use workflow_dispatch with epochs=1:
1. Go to Actions tab in GitHub
2. Select "ML Model Validation and Deployment Pipeline"
3. Click "Run workflow"
4. Set epochs to "1"
5. Click "Run workflow"

## Expected Results

### Success Scenario (epochs=10):
- ✅ Validate job: Trains model, accuracy ~97%, creates model_info.txt
- ✅ Deploy job: Threshold check passes, mock Docker build succeeds

### Failure Scenario (epochs=1):
- ✅ Validate job: Trains model, accuracy ~70%, creates model_info.txt
- ❌ Deploy job: Threshold check fails (accuracy < 85%), build skipped
