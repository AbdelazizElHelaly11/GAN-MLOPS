"""
Check if model accuracy meets the deployment threshold
Reads run ID from model_info.txt and checks accuracy in MLflow
"""
import os
import sys
import mlflow
from mlflow.tracking import MlflowClient


def check_threshold(threshold=0.85):
    """
    Check if the model accuracy meets the threshold
    
    Args:
        threshold: Minimum accuracy required (default: 0.85)
    
    Returns:
        bool: True if accuracy meets threshold, False otherwise
    """
    # Read the run ID and accuracy from model_info.txt
    try:
        with open("model_info.txt", "r") as f:
            lines = f.readlines()
            run_id = lines[0].strip()
            accuracy = float(lines[1].strip())
        print(f"Reading metrics from model_info.txt")
        print(f"Run ID: {run_id}")
    except (FileNotFoundError, IndexError, ValueError) as e:
        print(f"ERROR: Could not read model_info.txt: {e}")
        sys.exit(1)
        
        print(f"\n{'='*60}")
        print(f"Model Validation Check")
        print(f"{'='*60}")
        print(f"Run ID: {run_id}")
        print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Threshold: {threshold:.4f} ({threshold*100:.2f}%)")
        print(f"{'='*60}")
        
        # Check if accuracy meets threshold
        if accuracy >= threshold:
            print(f"✓ PASS: Model accuracy ({accuracy:.4f}) meets threshold ({threshold:.4f})")
            print(f"✓ Model is ready for deployment!")
            return True
        else:
            print(f"✗ FAIL: Model accuracy ({accuracy:.4f}) below threshold ({threshold:.4f})")
            print(f"✗ Model does NOT meet deployment criteria!")
            print(f"  Accuracy gap: {threshold - accuracy:.4f} ({(threshold - accuracy)*100:.2f}%)")
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: Failed to retrieve run metrics: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Get threshold from environment variable or use default
    threshold = float(os.getenv("ACCURACY_THRESHOLD", "0.85"))
    check_threshold(threshold)
