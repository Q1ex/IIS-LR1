 Heart Disease Prediction – Анализ и подготовка данных

## Описание проекта
Проект направлен на предварительный анализ и очистку данных для задачи **прогнозирования заболеваний сердца**.  
Используется базовый датасет **Heart Disease Prediction Dataset**, содержащий медицинские показатели пациентов (возраст, давление, уровень холестерина и др.).  

Задачи проекта:
- Загрузка и первичный анализ данных  
- Очистка и приведение данных к корректным типам  
- Анализ признаков и их взаимосвязи с целевой переменной  
- Сохранение финального очищенного датасета для последующего построения моделей  

---
## Структура проекта
К моменту выполнения ЛР4 структура проекта выглядит следующим образом:
```
lab_1iis
|_____ .venv_my_proj # виртуальное окружение
|_____ .git # локальный репозиторий
|_____ data # папка с исходными и промежуточными данными
| |___ dataset.csv # исходный датасет
| |___ clean_dataset.pkl # очищенный датасет
|
|_____ eda # папка с EDA
| |___ eda.ipynb # блокнот с разведочным анализом данных
|
|_____ graph # графики с EDA
|  |___ graph2.png
|  |___ ...
|
|_____ research # Ноутбук с графики исследований лучшей модели
|  |___ research.ipynb
|  |___ ...
|
|__ services                 # продакшн-часть: сервисы и мониторинг в Docker
|  |__ ml_service            # сервис для инференса обученной модели (FastAPI)
|  |  |__ main.py            # точка входа FastAPI-приложения, описание эндпоинтов
|  |  |__ api_handler.py     # обёртка для загрузки модели и выполнения predict
|  |  |__ requirements.txt   # зависимости, необходимые только для работы сервиса
|  |  |__ Dockerfile         # инструкция сборки Docker-образа ml_service
|  |
|  |__ requests              # сервис-генератор запросов к ml_service
|  |  |__ random_request.py  # скрипт отправки запросов к API
|  |  |__ requirements.txt   # зависимости генератора трафика
|  |  |__ Dockerfile         # сборка Docker-образа requests_service
|  |
|  |__ prometheus            # конфигурация Prometheus
|  |  |__ prometheus.yml     # описание jobs и targets (ml_service и др.)
|  |
|  |__ grafana               # файлы Grafana
|  |  |__ grafana.db         # база данных Grafana (дашборды, настройки)
|  |  |__ ml_dashboard.json  # экспортированный дашборд мониторинга
|  |  |__ ...                # служебные папки (csv, pdf, plugins, png)
|  |
|  |__ models                  # Артефакты обучения
|  |  |__ get_model.py         # Скрипт для получения модели из Mlflow
|  |  |__ model.pkl            # Обученная модель (RandomForest), используемая сервисом получить из скрипта
|
|_____ .gitignore
|_____ README.md
|_____ requirements.txt
```



## Как запустить проект
1. Установите зависимости:
   pip install -r "requirements.txt"


2. Скачайте датасет heart-disease.csv и положите его в папку проекта.


3. Запустите Jupyter Notebook:

jupyter notebook

и откройте файл heart_analysis.ipynb.


4. После выполнения ноутбука будут сохранены:

очищенный датасет: heart_clean.pkl

графики: plot1_target_distribution.png, plot2_numeric_histograms.png, plot3_correlation_heatmap.png, plot4_age_boxplot.png, plot5_age_vs_chol.png

интерактивный график: plot5_age_vs_chol.html

## Запуск MLflow
MLflow используется для логирования экспериментов и модели.  
1. Перейти в папку mlflow:
   cd mlflow

2. Запустить скрипт
   start_mlflow.sh

Сервер MLflow стартует локально на порту 5000.
Эксперименты и артефакты сохраняются в SQLite базе mlflow/mlruns.db



Результаты анализа

1. Распределение целевой переменной
Целевая переменная сбалансирована — данные подходят для моделирования без дополнительного балансирования.


2. Распределение числовых признаков

Возраст распределён близко к нормальному

Холестерин и некоторые другие показатели имеют смещение и выбросы



3. Корреляция признаков

Отсутствует сильная мультиколлинеарность

Есть умеренные связи (например, давление и возраст)



4. Boxplot возраста по целевой переменной
Пациенты с болезнью сердца в среднем младше 


5. Интерактивный график (возраст vs холестерин)

Повышенный холестерин чаще встречается у пациентов среднего и старшего возраста

У таких пациентов выше вероятность наличия болезни сердца






Результаты исследования

Наилучшее качество показала модель RandomForestClassifier с параметрами:
   n_estimators=157
   max_depth=12
   max_features=0.35281865781747324
   random_state=42

Получены следующие результаты:
   f1 - 0.81
   Precision - 0.74
   Recall - 0.9
   Roc_AUC - 0.87

Исследование проводилось на следующих столбцах:
   num__age, num__trestbps, num__chol, num__thalach, num__oldpeak;
   poly__age, poly__chol, poly__age^2, poly__age chol, poly__chol^2;
   kbins__thalach;
   cat__sex, cat__cp, cat__fbs, cat__restecg, cat__exang, cat__slope, cat__ca, cat__thal;

   Run_id prod модели: 9ccf6e5a74574f1aad71e76d7b5d0201




---

Выводы

Данные очищены от дубликатов, проверены на пропуски и выбросы

Столбцы приведены к корректным типам

Выделены числовые и категориальные признаки



# ЛР 3 Создание сервиса предсказаний

## Описание сервиса

Папка `services/ml_service` содержит код REST‑сервиса для инференса модели:  
- `main.py` – FastAPI‑приложение с endpointом `/api/prediction/{item_id}`, описанием входных полей и формированием `pandas.DataFrame` для модели. 
- `api_handler.py` – обёртка над загруженной моделью (`joblib.load`), выполняющая предсказание по переданным признакам.
- `requirements.txt` – минимальные зависимости, необходимые только для работы сервиса (FastAPI, Uvicorn, pandas, numpy, scikit‑learn, joblib и др.).
- `Dockerfile` – рецепт сборки Docker‑образа на базе `python:3.10-slim` и команды для запуска Uvicorn внутри контейнера.

Папка `models` содержит файл обученной модели:  
- `model.pkl` – сериализованный RandomForest‑классификатор (или pipeline), который используется сервисом для предсказаний.

## Сборка Docker‑образа

Из директории `services/ml_service`:

```bash
docker build -t heart_ml_service:1.0 .
```

Здесь `heart_ml_service` – имя образа, `1.0` – первая версия образа согласно заданию.

## Запуск контейнера

Из той же директории:

```bash
docker run -p 8000:8000 -v "$(pwd)/../models:/models" --name heart_ml_service_container heart_ml_service:1.0
```

- `-p 8000:8000` – пробрасывает порт `8000` контейнера на порт `8000` хоста (доступ по `http://localhost:8000`).
- `-v "$(pwd)/../models:/models"` – монтирует локальную папку `../models` в `/models` внутри контейнера, откуда код загружает `model.pkl`.

## Проверка работоспособности

1. Открыть браузер и перейти по адресу:  
   `http://localhost:8000/docs` – автоматически сгенерированная Swagger‑документация FastAPI.
2. Найти метод `POST /api/prediction/{item_id}`, нажать **Try it out**, указать `item_id` (например, `"1"`).  
3. Вставить пример тела запроса:

```json
{
  "age": 62,
  "sex": 1,
  "cp": 0,
  "trestbps": 140,
  "chol": 280,
  "fbs": 0,
  "restecg": 0,
  "thalach": 115,
  "exang": 1,
  "oldpeak": 1.5,
  "slope": 1,
  "ca": 3,
  "thal": 2,
  "high_age": 1
}
```

4. Нажать **Execute** и убедиться, что сервис возвращает JSON с полями `item_id` и `predict` (классификация по обученной модели).

   Пример полученного ответа:
   ```json
   {
     "item_id": "1",
     "predict": 0
   }
   ```

# Лабораторная работа №4. Мониторинг сервиса с моделью

В рамках ЛР4 к ранее разработанному сервису машинного обучения добавлен стек мониторинга на базе Prometheus и Grafana.  


***

## Используемые технологии

- Python, FastAPI — реализация REST‑сервиса с моделью.  
- scikit-learn / pickle — загрузка и применение обученной модели.  
- Prometheus + библиотека prometheus_client — сбор и экспозиция метрик сервиса.  
- Grafana — визуализация метрик и построение дашборда.  
- Docker, Docker Compose — упаковка сервисов и их совместный запуск.  

***

## Структура сервисов для мониторинга

Папка `services/`:

- `ml_service/`  
  - `main.py` — FastAPI‑приложение, эндпоинт для предсказаний, экспозиция метрик `/metrics`.  
  - `api_handler.py` (если есть) — вспомогательная логика обработки запросов.  
  - `models/` — сериализованная модель, используемая сервисом.  
  - `Dockerfile` — образ сервиса `ml_service`.  
  - Сервис поднимается на `http://ml_service:8000` (снаружи: `http://localhost:8000`), Swagger: `/docs`.

- `requests/`  
  - Скрипт(ы) генерации трафика к `ml_service` (периодические HTTP‑запросы для нагрузки и генерации метрик).  
  - `Dockerfile` — образ `requests_service`.  
  - Веб‑интерфейса нет, сервис работает в фоне.

- `prometheus/`  
  - `prometheus.yml` — конфигурация Prometheus: job для опроса `ml_service:8000/metrics` и других target‑ов при необходимости.  
  - Образ: `prom/prometheus:latest`.  
  - Веб‑интерфейс Prometheus: `http://localhost:9090`.

- `grafana/`  
  - `ml_dashboard.json` — экспортированный дашборд Grafana с панелями мониторинга.  
  - (При необходимости) папка данных Grafana, смонтированная в `/var/lib/grafana`.  
  - Образ: `grafana/grafana:latest`.  
  - Веб‑интерфейс Grafana: `http://localhost:3000`, логин/пароль: `admin/admin`.

Сервисы `database` и `pgadmin` в рамках данной лабораторной работы не поднимались, задания, связанные с БД, не выполнялись (по условию это допускается).

***

## Docker Compose и запуск проекта

Файл `services/compose.yml` описывает совместный запуск:

- `ml_service` — сервис с моделью.  
- `requests_service` — генератор запросов.  
- `prometheus` — сборщик метрик.  
- `grafana` — визуализация.

Запуск проекта:

```bash
cd services
docker compose -f compose.yml up --build
```

Остановка:

```bash
cd services
docker compose -f compose.yml down
```

После запуска сервисы доступны по адресам:

- ML‑сервис: `http://localhost:8000/docs` (Swagger)  
- Prometheus: `http://localhost:9090`  
- Grafana: `http://localhost:3000` (admin / admin)

***

## Метрики и мониторинг (Prometheus)

В `ml_service` реализованы пользовательские метрики, экспонируемые на `/metrics`, например:

- `ml_requests_total` — общее число запросов к API (counter).  
- `ml_requests_error_total{status="..."}` — количество ошибочных запросов по статус‑коду (4xx, 5xx).  
- `model_prediction_bucket` — гистограмма/бакеты распределения предсказаний модели.  
- `process_cpu_seconds_total`, `process_resident_memory_bytes` — инфраструктурные метрики процесса.

Примеры запросов в Prometheus:

- Частота запросов к сервису (RPS):

  ```promql
  avg(rate(ml_requests_total[1m]))
  avg(rate(ml_requests_total[1h]))
  ```

- Ошибки 4xx и 5xx (в минуту):

  ```promql
  sum(rate(ml_requests_error_total{status=~"4..|5.."}[1m]) * 60) by (status)
  ```

- Распределение предсказаний по классам через бакеты:

  ```promql
  rate(model_prediction_bucket{le="1.5"}[1m]) * 60
  rate(model_prediction_bucket{le="0.5"}[1m]) * 60
  (avg(rate(model_prediction_bucket{le="1.5"}[1m])) - avg(rate(model_prediction_bucket{le="0.5"}[1m]))) * 60
  ```

- Использование CPU:

  ```promql
  rate(process_cpu_seconds_total[1m])
  ```

- Использование памяти в МБ:

  ```promql
  process_resident_memory_bytes / 1048576
  ```

Скриншоты с графиками Prometheus прикладываются в репозиторий и демонстрируют поведение этих метрик под нагрузкой.

### Гистограма предсказаний модели
![ml_predict_lr4.png](images%2Fml_predict_lr4.png)

### Частота (rate) запросов к основному сервису в минуту
![req_rate_prometheus_lr4.png](images%2Freq_rate_prometheus_lr4.png)

### Количество запросов к сервису с кодами ошибок 4** и 5** (две линии на одном графике).
![req_errors_lr4.png](images%2Freq_errors_lr4.png)


***

## Дашборд Grafana

В Grafana создан отдельный дашборд (экспортирован в `services/grafana/ml_dashboard.json`), который использует источник данных Prometheus (`http://prometheus:9090`).  
Дашборд содержит минимум 5 графиков разных уровней мониторинга.

Основные панели:

1. «Requests rate (RPS)» — прикладной уровень  
   - Запросы:

        `avg(rate(ml_requests_total[1m]))`

        `avg(rate(ml_requests_total[1h]))`  

   - Показывает частоту запросов к API, сглаженную по окну 1 минута и 1 час.

2. «4xx and 5xx errors» — прикладной уровень  
   - Запрос: `sum(rate(ml_requests_error_total{status=~"4..|5.."}[1m]) * 60) by (status)`  
   - Две линии: частота ошибок с кодами 4xx и 5xx, в ошибках в минуту.

3. «Predictions rate by class» — уровень качества модели / data shift  
   - Запросы на основе `model_prediction_bucket`, например:  
     - класс 0: `rate(model_prediction_bucket{le="0.5"}[1m]) * 60`  
     - класс 1: разность бакетов `(avg(rate(model_prediction_bucket{le="1.5"}[1m])) - avg(rate(model_prediction_bucket{le="0.5"}[1m]))) * 60`  
   - По изменению соотношения классов во времени можно судить о возможном data shift.

4. «ML service CPU usage (seconds/s)» — инфраструктурный уровень  
   - Запрос: `rate(process_cpu_seconds_total[1m])`  
   - Отражает загрузку CPU процессом сервиса.

5. «ML service memory usage (MiB)» — инфраструктурный уровень  
   - Запрос: `process_resident_memory_bytes / 1048576` с единицами оси в MiB.  
   - Показывает потребление оперативной памяти сервисом.

Скриншот итогового дашборда (`images/grafana_dashboard.png`) добавлен в репозиторий и демонстрирует работу всех панелей одновременно.
![dashboard.png](images%2Fdashboard.png)
***

## Импорт/экспорт дашборда

- Для экспорта дашборда из Grafana используется меню Dashboard settings → JSON model → Download JSON, файл сохранён как `grafana/ml_dashboard.json`.  
- Для повторного использования дашборда его можно импортировать через Grafana: Dashboards → Import → Upload JSON file → выбрать `ml_dashboard.json`.