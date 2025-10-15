#!/bin/bash
# Скрипт запуска локального MLflow с SQLite-хранилищем

# Убедимся, что находимся в директории mlflow
cd "$(dirname "$0")"

# Запускаем mlflow с указанием БД и папки для логов
mlflow server \
  --backend-store-uri sqlite:///mlruns.db \
  --default-artifact-root ./artifacts \
  --host 127.0.0.1 \
  --port 5000
