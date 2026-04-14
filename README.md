# GAN-MLOPS Assignment Pipeline

This repository implements a two-job GitHub Actions MLOps pipeline:

1. **Validate job** trains an MNIST classifier, logs metrics to MLflow, and exports `model_info.txt` with the MLflow run ID.
2. **Deploy job** downloads artifacts, validates `accuracy >= 0.85` via `check_threshold.py`, and runs a mock Docker build.

## Key Files

- `.github/workflows/pipeline.yml`
- `train.py`
- `check_threshold.py`
- `Dockerfile`
- `data.dvc`

## Local Test

Run from PowerShell in the repo root:

```powershell
$env:MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
$env:EPOCHS = "10"
python train.py

$env:ACCURACY_THRESHOLD = "0.85"
python check_threshold.py
```

To force a failure case, run training with `EPOCHS=1` and then run `check_threshold.py`.

# Assignment 6 Complete: Gatekeeper Workflow Implementation

