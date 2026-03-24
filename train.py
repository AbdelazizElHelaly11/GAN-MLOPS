"""
Simple MNIST classifier that logs to MLflow
Configurable epochs via EPOCHS environment variable for testing
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import mlflow
import mlflow.tensorflow


def load_data():
    """Load and preprocess MNIST data"""
    print("Loading MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    
    # Normalize pixel values
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    
    # Reshape for Dense layers
    x_train = x_train.reshape(-1, 784)
    x_test = x_test.reshape(-1, 784)
    
    print(f"Training samples: {len(x_train)}, Test samples: {len(x_test)}")
    return (x_train, y_train), (x_test, y_test)


def build_model():
    """Build a simple feedforward neural network"""
    model = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=(784,)),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(10, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def train():
    """Train the model and log to MLflow"""
    # Get epochs from environment variable (default 10 for high accuracy)
    epochs = int(os.getenv('EPOCHS', '10'))
    batch_size = 128
    
    print(f"\n{'='*60}")
    print(f"Training Configuration:")
    print(f"  Epochs: {epochs}")
    print(f"  Batch Size: {batch_size}")
    print(f"{'='*60}\n")
    
    # Set MLflow experiment
    mlflow.set_experiment("MNIST_Classification")
    
    with mlflow.start_run() as run:
        # Get the run ID
        run_id = run.info.run_id
        print(f"MLflow Run ID: {run_id}")
        
        # Log parameters
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("optimizer", "adam")
        mlflow.set_tag("model_type", "feedforward_classifier")
        
        # Load data
        (x_train, y_train), (x_test, y_test) = load_data()
        
        # Build and train model
        print("\nBuilding model...")
        model = build_model()
        
        print("\nTraining model...")
        history = model.fit(
            x_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_split=0.1,
            verbose=1
        )
        
        # Evaluate on test set
        print("\nEvaluating model...")
        test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
        
        # Log metrics
        mlflow.log_metric("test_loss", test_loss)
        mlflow.log_metric("test_accuracy", test_accuracy)
        mlflow.log_metric("accuracy", test_accuracy)  # Key metric for threshold check
        
        # Log final training accuracy
        final_train_acc = history.history['accuracy'][-1]
        mlflow.log_metric("train_accuracy", final_train_acc)
        
        print(f"\n{'='*60}")
        print(f"Training Results:")
        print(f"  Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        print(f"  Test Loss: {test_loss:.4f}")
        print(f"  Final Training Accuracy: {final_train_acc:.4f}")
        print(f"{'='*60}\n")
        
        # Log the model
        print("Logging model to MLflow...")
        mlflow.tensorflow.log_model(
            model=model,
            artifact_path="model",
            registered_model_name="mnist_classifier"
        )
        
        # Export run ID to file
        print(f"Exporting run ID to model_info.txt...")
        with open("model_info.txt", "w") as f:
            f.write(run_id)
        
        print(f"\n✓ Training complete! Run ID: {run_id}")
        print(f"✓ Accuracy: {test_accuracy:.4f} - Threshold check: {'PASS' if test_accuracy >= 0.85 else 'FAIL'}")
        
        return run_id, test_accuracy


if __name__ == "__main__":
    try:
        run_id, accuracy = train()
        print(f"\nSuccess! Model trained with accuracy: {accuracy:.4f}")
    except Exception as e:
        print(f"\nError during training: {e}")
        raise
