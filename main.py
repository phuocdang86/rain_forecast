import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger
from pydantic import BaseModel
from date_transformer import DateCyclicalTransformer

app = FastAPI()

class WeatherFeatures(BaseModel):
    Date: str = '2014-03-25'
    Location: str = 'CoffsHarbour'
    MinTemp: float = 17.5
    MaxTemp: float = 24.4
    Rainfall: float = 16.8
    Evaporation: float = 3.4
    Sunshine: float = 0.9
    WindGustDir: str = 'SE'
    WindGustSpeed: float = 15.0
    WindDir9am: str = 'WSW'
    WindDir3pm: str = 'SE'
    WindSpeed9am: float = 7.0
    WindSpeed3pm: float = 9.0
    Humidity9am: float = 89.0
    Humidity3pm: float = 73.0
    Pressure9am: float = 1019.0
    Pressure3pm: float = 1018.7
    Cloud9am: float = 7.0
    Cloud3pm: float = 8.0
    Temp9am: float = 20.5
    Temp3pm: float = 23.8
    RainToday: str = 'Yes'

# Update the model path to reference the correct location
model_path = os.path.join(os.path.dirname(__file__), 'models', 'model.pkl')

try:
    model = joblib.load(model_path)
    logger.info(f"Model loaded from {model_path}")
except Exception as e:
    logger.error(f"Failed to load model from {model_path}: {e}")
    raise HTTPException(status_code=500, detail=f"Failed to load model: {e}")

@app.get("/")
def check_health():
    return {"status": "Ok"}

@app.post("/predict")
def predict(data: WeatherFeatures):
    try:
        logger.info("Making predictions...")
        data_dict = jsonable_encoder(data)
        data_df = pd.DataFrame([data_dict])
        result = model.predict(data_df)[0]
        if int(result) == 1:
            return {"Rain Tomorrow" : "Yes"}
        else:
            return {"Rain Tomorrow" : "No"}
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
