# GAN Project

## Overview
This project implements a Generative Adversarial Network (GAN) for image generation and processing.

## Project Structure
- `StudentA.py` - Main GAN implementation
- `requirements.txt` - Python dependencies
- `generator_model/` - Trained generator model artifacts
- `generated/` - Output directory for generated images
- `Dockerfile` - Container configuration for deployment
- `environment.yml` - Conda environment specification

## Dependencies
- TensorFlow >= 2.15.0
- NumPy >= 1.26.4
- Matplotlib >= 3.8.2

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python StudentA.py
```

## Model Training
The project uses MLflow for experiment tracking and logging. Training runs are saved in the `mlruns/` directory.

## Generated Outputs
Generated images are saved to the `generated/` directory during model execution.

## Docker Support
Build and run the project in a Docker container:
```bash
docker build -t gan-project .
docker run gan-project
```

## Environment
You can also set up the environment using Conda:
```bash
conda env create -f environment.yml
```

## License
This project is part of an academic assignment.
