FROM python:3.10-slim

# Accept RUN_ID as build argument
ARG RUN_ID
ENV RUN_ID=${RUN_ID}

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Simulate model download using RUN_ID
# In production, this would download from MLflow registry
RUN if [ -n "$RUN_ID" ]; then \
        echo "Simulating model download for Run ID: ${RUN_ID}" && \
        echo "In production: mlflow artifacts download --run-id ${RUN_ID} --artifact-path model --dst-path ./model" && \
        mkdir -p ./model && \
        echo "${RUN_ID}" > ./model/run_id.txt; \
    else \
        echo "No RUN_ID provided, skipping model download"; \
    fi

# Default command
CMD ["python", "train.py"]