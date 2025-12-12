import joblib
import pandas as pd
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int
    high_age: int


class FastAPIHandler:
    def __init__(self, modelpath: str):
        """
        Инициализация класса:
        Загружаем весь pipeline, включая все этапы предобработки и модель.
        """
        # Загружаем обученную модель (pipeline)
        self.model_path = modelpath
        self.model = joblib.load(modelpath)
        print(f"Модель загружена из {modelpath}")

    def _request_to_df(self, request: PredictionRequest) -> pd.DataFrame:
        """Конвертирует Pydantic request в DataFrame с правильным порядком колонок"""
        data = {
            'age': request.age,
            'sex': request.sex,
            'cp': request.cp,
            'trestbps': request.trestbps,
            'chol': request.chol,
            'fbs': request.fbs,
            'restecg': request.restecg,
            'thalach': request.thalach,
            'exang': request.exang,
            'oldpeak': request.oldpeak,
            'slope': request.slope,
            'ca': request.ca,
            'thal': request.thal,
            'high_age': request.high_age
        }

        features_df = pd.DataFrame([data])
        return features_df

    def predict(self, request: PredictionRequest) -> float:
        """
        Предсказание из Pydantic request
        """
        features_df = self._request_to_df(request)
        prediction = self.model.predict(features_df)[0]
        return int(prediction)