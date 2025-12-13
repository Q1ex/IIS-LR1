
import pandas as pd
from fastapi import FastAPI, HTTPException
from api_handler import FastAPIHandler, PredictionRequest

from prometheus_client import Histogram, Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / 'models' / 'model.pkl'

app = FastAPI()
handler = FastAPIHandler(modelpath=MODEL_PATH)

prediction_histogram = Histogram(
    "model_prediction",
    "Distribution of model predictions (0 - no disease, 1 - disease)",
    buckets=[-0.5, 0.5, 1.5]  # три корзины: <0.5, 0.5–1.5, >1.5
)

request_counter = Counter(
    "ml_requests_total",
    "Total number of requests to prediction endpoint",
    ["status"]
)

error_counter = Counter(
    "ml_requests_error_total",
    "Total number of error responses from prediction endpoint",
    ["status"]
)



@app.get("/")
async def read_root():
    print("### MAIN.PY LOADED ###")
    return {"Hello": "World"}



@app.post("/api/prediction/{item_id}")
async def predict(item_id: str, request: PredictionRequest):
    try:
        prediction = handler.predict(request)
        # записываем предсказание в гистограмму
        prediction_histogram.observe(prediction)

        # успешный запрос
        request_counter.labels(status="200").inc()
        
        return {
            "item_id": item_id,
            "predict": prediction
        }
    except HTTPException as e:
        # если сам бросишь HTTPException с 4xx/5xx
        request_counter.labels(status=str(e.status_code)).inc()
        if 400 <= e.status_code < 600:
            error_counter.labels(status=str(e.status_code)).inc()
        raise
    except Exception:
        traceback.print_exc()
                # 500
        request_counter.labels(status="500").inc()
        error_counter.labels(status="500").inc()
        raise HTTPException(status_code=500,
                                detail="Something went wrong. Check logs for more details")

@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.get("/test_error/{code}")
async def test_error(code: int):
    """
    Args:
        code: get Error to check monitoring state

    Returns: Optional[Exception]

    """
    if code == 400:
        request_counter.labels(status="400").inc()
        error_counter.labels(status="400").inc()
        raise HTTPException(status_code=400, detail="Test 400 error")
    elif code == 500:
        request_counter.labels(status="500").inc()
        error_counter.labels(status="500").inc()
        raise HTTPException(status_code=500, detail="Test 500 error")
    else:
        request_counter.labels(status="200").inc()
        return {"message": "No error"}
    
    
    