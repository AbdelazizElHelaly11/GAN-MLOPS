"""
Check if model accuracy meets the deployment threshold.
Reads run ID from model_info.txt and checks metrics in MLflow.
"""
import os
import sys

from mlflow.exceptions import MlflowException
from mlflow.tracking import MlflowClient


def read_run_id(path="model_info.txt"):
    """Read run ID from the first line of model_info.txt."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            run_id = file.readline().strip()
    except FileNotFoundError as error:
        print(f"ERROR: Could not read {path}: {error}")
        sys.exit(1)

    if not run_id:
        print(f"ERROR: {path} is empty or does not contain a run ID.")
        sys.exit(1)

    return run_id


def fetch_accuracy(run_id):
    """Fetch accuracy metric from MLflow by run ID."""
    client = MlflowClient()

    try:
        run = client.get_run(run_id)
    except MlflowException as error:
        print(f"ERROR: Could not retrieve MLflow run '{run_id}': {error}")
        sys.exit(1)

    metrics = run.data.metrics
    if "accuracy" in metrics:
        return float(metrics["accuracy"])
    if "test_accuracy" in metrics:
        return float(metrics["test_accuracy"])

    available_metrics = ", ".join(sorted(metrics.keys())) if metrics else "none"
    print(
        f"ERROR: No 'accuracy' or 'test_accuracy' metric found for run {run_id}. "
        f"Available metrics: {available_metrics}"
    )
    sys.exit(1)


def check_threshold(threshold=0.85):
    """Validate model performance against the deployment threshold."""
    run_id = read_run_id()
    accuracy = fetch_accuracy(run_id)

    print(f"\n{'='*60}")
    print("Model Validation Check")
    print(f"{'='*60}")
    print(f"Run ID: {run_id}")
    print(f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Threshold: {threshold:.4f} ({threshold * 100:.2f}%)")
    print(f"{'='*60}")

    if accuracy >= threshold:
        print(f"PASS: Model accuracy ({accuracy:.4f}) meets threshold ({threshold:.4f})")
        print("Model is ready for deployment.")
        return True

    print(f"FAIL: Model accuracy ({accuracy:.4f}) below threshold ({threshold:.4f})")
    print("Model does NOT meet deployment criteria.")
    print(f"Accuracy gap: {threshold - accuracy:.4f} ({(threshold - accuracy) * 100:.2f}%)")
    sys.exit(1)


if __name__ == "__main__":
    try:
        threshold_value = float(os.getenv("ACCURACY_THRESHOLD", "0.85"))
    except ValueError as error:
        print(f"ERROR: Invalid ACCURACY_THRESHOLD value: {error}")
        sys.exit(1)

    check_threshold(threshold_value)
