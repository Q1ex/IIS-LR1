#модель собиралась на python 3.10 и при использовании 3.11 возникала ошибка при запуске контейнера
FROM python:3.10-slim

# 1. Скопировать всё из текущей директории в /ml_service
COPY . /ml_service

# 2. Директория с моделями, доступная снаружи
VOLUME ["/models"]

# 3. Рабочая директория
WORKDIR /ml_service

# 4. Установка зависимостей
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. Открыть 8000
EXPOSE 8000

# 6. Команда запуска сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# команда сборки образа
# docker build -t heart_ml_service:1.0 .

# Команда запуска контейнера.
# docker run -p 8000:8000 -v "$(pwd)/../models:/models" --name heart_ml_service_container heart_ml_service:1.0

