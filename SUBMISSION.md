# ML Pipeline Assignment - Submission

## Assignment Completion Summary

All required components have been successfully implemented for the multi-job GitHub Actions pipeline.

---

## 📁 Deliverables

### 1. The YAML File
**Location**: `.github/workflows/pipeline.yml`

**Features**:
- ✅ Two-job pipeline (validate → deploy)
- ✅ Validate job: DVC pull, train model, log to MLflow, export Run ID
- ✅ Deploy job: Check threshold, mock Docker build
- ✅ Artifact passing between jobs
- ✅ Manual trigger with configurable epochs

### 2. Supporting Files

#### train.py
- Simple MNIST classifier (feedforward neural network)
- Logs to MLflow (accuracy, loss, parameters)
- Exports Run ID to `model_info.txt`
- Configurable via `EPOCHS` environment variable
- **Low accuracy**: Set EPOCHS=1 or 2 (~70-80% accuracy)
- **High accuracy**: Set EPOCHS=10 (~97% accuracy)

#### check_threshold.py
- Reads Run ID from `model_info.txt`
- Queries MLflow for accuracy metric
- Fails pipeline if accuracy < 0.85
- Clear pass/fail messaging

#### Dockerfile
- Base: `python:3.10-slim`
- Accepts `ARG RUN_ID`
- Simulates model download using Run ID
- Production-ready structure

#### data.dvc
- DVC tracking file for data versioning
- Pipeline includes `dvc pull` step

---

## 🧪 Testing Instructions

### How to Generate Screenshots

#### For FAILED Run Screenshot (accuracy < 85%):

1. Go to your GitHub repository
2. Navigate to **Actions** tab
3. Click **ML Model Validation and Deployment Pipeline**
4. Click **Run workflow** button
5. In the dropdown:
   - Branch: `ci-test` or `main`
   - Epochs: Enter `1`
6. Click **Run workflow**
7. Wait for pipeline to complete
8. **Expected Result**:
   - ✅ Validate job: SUCCESS (trains but low accuracy)
   - ❌ Deploy job: FAILURE (threshold check fails)
9. Take screenshot showing the failed deploy job

#### For SUCCESSFUL Run Screenshot (accuracy > 85%):

1. Go to your GitHub repository
2. Navigate to **Actions** tab
3. Click **ML Model Validation and Deployment Pipeline**
4. Click **Run workflow** button
5. In the dropdown:
   - Branch: `ci-test` or `main`
   - Epochs: Enter `10` (or leave default)
6. Click **Run workflow**
7. Wait for pipeline to complete
8. **Expected Result**:
   - ✅ Validate job: SUCCESS (trains with high accuracy)
   - ✅ Deploy job: SUCCESS (threshold passes, mock build runs)
9. Take screenshot showing both jobs successful with green checkmarks

### Alternative: Push to Trigger

```bash
# Commit and push to trigger with default settings (10 epochs = success)
git add .
git commit -m "test: ML pipeline implementation"
git push origin ci-test
```

---

## 📊 Expected Outputs

### Validate Job Output:
```
Training with 10 epochs...
Loading MNIST dataset...
Training samples: 60000, Test samples: 10000
Building model...
Training model...
Epoch 1/10 ... Epoch 10/10
Evaluating model...
Test Accuracy: 0.9745 (97.45%)
✓ Training complete! Run ID: abc123def456
✓ Accuracy: 0.9745 - Threshold check: PASS
```

### Deploy Job Output (Success):
```
Checking if model meets deployment threshold...
Run ID: abc123def456
Accuracy: 0.9745 (97.45%)
Threshold: 0.8500 (85.00%)
✓ PASS: Model accuracy (0.9745) meets threshold (0.8500)
✓ Model is ready for deployment!

Building Docker image for Run ID: abc123def456
✓ Mock build successful!
```

### Deploy Job Output (Failure):
```
Checking if model meets deployment threshold...
Run ID: xyz789abc012
Accuracy: 0.7234 (72.34%)
Threshold: 0.8500 (85.00%)
✗ FAIL: Model accuracy (0.7234) below threshold (0.8500)
✗ Model does NOT meet deployment criteria!
  Accuracy gap: 0.1266 (12.66%)
Error: Process completed with exit code 1.
```

---

## 🔧 Technical Details

### Pipeline Architecture

```
┌─────────────────────────────────────┐
│         VALIDATE JOB                │
├─────────────────────────────────────┤
│ 1. Checkout code                    │
│ 2. Setup Python 3.10                │
│ 3. Install dependencies             │
│ 4. DVC pull (data)                  │
│ 5. Train model → MLflow             │
│ 6. Export Run ID → model_info.txt   │
│ 7. Upload artifacts                 │
│    - model_info.txt                 │
│    - mlruns/                        │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│         DEPLOY JOB                  │
├─────────────────────────────────────┤
│ 1. Checkout code                    │
│ 2. Setup Python 3.10                │
│ 3. Install MLflow                   │
│ 4. Download artifacts               │
│    - model_info.txt                 │
│    - mlruns/                        │
│ 5. Check threshold (Python script)  │
│    ├─ Read Run ID                   │
│    ├─ Query MLflow                  │
│    └─ Validate accuracy ≥ 0.85      │
│ 6. Mock Docker build (if passed)    │
│    └─ echo "Building with RUN_ID"   │
└─────────────────────────────────────┘
```

### Key Features

1. **Artifact Passing**: Uses `actions/upload-artifact@v4` and `actions/download-artifact@v4` to pass Run ID between jobs
2. **Threshold Validation**: Python script with clear error handling and exit codes
3. **Conditional Execution**: Deploy job only runs if validate succeeds; build only runs if threshold passes
4. **Configurable Testing**: Manual workflow trigger with epochs input for easy testing
5. **MLflow Integration**: Local tracking with artifact upload for persistence

---

## 📝 Submission Checklist

- [x] **pipeline.yml** - Complete two-job workflow
- [x] **train.py** - MNIST classifier with MLflow logging
- [x] **check_threshold.py** - Threshold validation script
- [x] **Dockerfile** - With RUN_ID argument
- [x] **data.dvc** - DVC tracking file
- [ ] **Screenshot 1** - Failed run (accuracy < 85%)
- [ ] **Screenshot 2** - Successful run (accuracy > 85%)

---

## 🚀 Next Steps

1. Push all changes to GitHub:
   ```bash
   cd "C:\Users\hzezo\OneDrive\Desktop\gan_project"
   git add .
   git commit -m "feat: implement multi-job ML pipeline with threshold validation"
   git push origin ci-test
   ```

2. Generate failed run screenshot (epochs=1)
3. Generate successful run screenshot (epochs=10)
4. Submit YAML file + screenshots

---

## 📞 Troubleshooting

**Issue**: Validate job fails during training
- Check Python dependencies are installed
- Verify tensorflow can be imported

**Issue**: Deploy job can't find artifacts
- Check artifact names match between upload and download
- Verify validate job completed successfully

**Issue**: Threshold check fails unexpectedly
- Check mlruns directory was uploaded
- Verify model_info.txt contains valid Run ID
- Check MLFLOW_TRACKING_URI is set correctly

---

Generated: 2026-03-24
