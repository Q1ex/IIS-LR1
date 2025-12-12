
import pandas as pd
from fastapi import FastAPI, HTTPException
from api_handler import FastAPIHandler, PredictionRequest

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / 'models' / 'model.pkl'

app = FastAPI()
handler = FastAPIHandler(modelpath=MODEL_PATH)
@app.get("/")
async def read_root():
    print("### MAIN.PY LOADED ###")
    return {"Hello": "World"}


@app.post("/api/prediction/{item_id}")
async def predict(item_id: str, request: PredictionRequest):
    try:
        prediction = handler.predict(request)
        return {
            "item_id": item_id,
            "predict": prediction
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail='Something went wrong. Check logs for more details')