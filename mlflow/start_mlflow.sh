#!/bin/bash

# --- Настройки ---
TRACKING_SERVER_HOST="127.0.0.1"
TRACKING_SERVER_PORT=5000
TRACKING_DB="./mlflow.db"
ARTIFACT_ROOT="./mlruns"

# --- Формируем URI ---
TRACKING_URI="http://${TRACKING_SERVER_HOST}:${TRACKING_SERVER_PORT}"
REGISTRY_URI="http://${TRACKING_SERVER_HOST}:${TRACKING_SERVER_PORT}"

# --- Запуск MLflow сервера в фоне ---
echo "Starting MLflow server..."
mlflow server \
    --backend-store-uri sqlite:///$TRACKING_DB \
    --default-artifact-root $ARTIFACT_ROOT \
    --host $TRACKING_SERVER_HOST \
    --port $TRACKING_SERVER_PORT &
    
echo "MLflow server started at $TRACKING_URI"
echo "Open MLflow UI in browser: http://${TRACKING_SERVER_HOST}:${TRACKING_SERVER_PORT}"