"""
Check if model accuracy meets the deployment threshold.
Reads run ID from model_info.txt and checks metrics in MLflow.
"""
import os
import sys
from pathlib import Path

import mlflow
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


def discover_file_tracking_uris(run_id):
    """
    Discover local file-store tracking URIs that contain the requested run.
    This handles artifact layouts where mlruns may be nested after download.
    """
    uris = []
    for meta_file in Path(".").glob(f"**/{run_id}/meta.yaml"):
        # Expected layout: <tracking_dir>/<experiment_id>/<run_id>/meta.yaml
        tracking_dir = meta_file.parents[2]
        posix_path = tracking_dir.as_posix()
        uris.append(posix_path)
        uris.append(f"file:{posix_path}")
    return uris


def build_tracking_uri_candidates(run_id):
    """Build tracking URI candidates in fallback order."""
    candidates = []
    env_uri = os.getenv("MLFLOW_TRACKING_URI", "").strip()
    if env_uri:
        candidates.append(env_uri)

    candidates.extend(
        [
            "sqlite:///mlflow.db",
            "./mlruns",
            "file:./mlruns",
        ]
    )
    candidates.extend(discover_file_tracking_uris(run_id))

    unique = []
    seen = set()
    for uri in candidates:
        if uri and uri not in seen:
            seen.add(uri)
            unique.append(uri)
    return unique


def extract_accuracy(run):
    """Extract accuracy from supported metric names in a run."""
    metrics = run.data.metrics
    if "accuracy" in metrics:
        return float(metrics["accuracy"])
    if "test_accuracy" in metrics:
        return float(metrics["test_accuracy"])

    available_metrics = ", ".join(sorted(metrics.keys())) if metrics else "none"
    print(
        "ERROR: No 'accuracy' or 'test_accuracy' metric found for run "
        f"{run.info.run_id}. Available metrics: {available_metrics}"
    )
    sys.exit(1)


def fetch_accuracy(run_id):
    """Fetch accuracy metric from MLflow by run ID."""
    attempted = []
    for tracking_uri in build_tracking_uri_candidates(run_id):
        mlflow.set_tracking_uri(tracking_uri)
        client = MlflowClient()
        try:
            run = client.get_run(run_id)
            return extract_accuracy(run), tracking_uri
        except MlflowException as error:
            attempted.append(f"{tracking_uri}: {error}")

    attempted_text = "\n".join(f"  - {entry}" for entry in attempted[:5])
    print(
        f"ERROR: Could not retrieve MLflow run '{run_id}' from available tracking URIs.\n"
        f"Attempted:\n{attempted_text}"
    )
    sys.exit(1)


def check_threshold(threshold=0.85):
    """Validate model performance against the deployment threshold."""
    run_id = read_run_id()
    accuracy, tracking_uri = fetch_accuracy(run_id)

    print(f"\n{'='*60}")
    print("Model Validation Check")
    print(f"{'='*60}")
    print(f"Run ID: {run_id}")
    print(f"Tracking URI: {tracking_uri}")
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
