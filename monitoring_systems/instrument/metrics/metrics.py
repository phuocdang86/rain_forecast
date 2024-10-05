# Read more about OpenTelemetry here:
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
from io import BytesIO
from time import time
import os
import sys
import joblib
import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from prometheus_client import start_http_server
from pydantic import BaseModel

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Notebooks')))
from date_transformer import DateCyclicalTransformer

# Start Prometheus client
start_http_server(port=8099, addr="0.0.0.0")

# Service name is required for most backends
resource = Resource(attributes={SERVICE_NAME: "rain-prediction-service"})

# Exporter to export metrics to Prometheus
reader = PrometheusMetricReader()

# Meter is responsible for creating and recording metrics
provider = MeterProvider(resource=resource, metric_readers=[reader])
set_meter_provider(provider)
meter = metrics.get_meter("rain-prediction", "1.0.0")

# Create your first counter
counter = meter.create_counter(
    name="Service_request_counter", description="Number of service requests"
)

histogram = meter.create_histogram(
    name="Service_response_histogram",
    description="Service response histogram",
    unit="seconds",
)


# Class to define the request body
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


# Load model
model = joblib.load("../../../models/model.pkl")

app = FastAPI()

# Create an endpoint to check API health
@app.get("/")
def check_health():
    return {"status": "Oke"}


# Create an endpoint to make a prediction
@app.post("/predict")
def predict(data: WeatherFeatures):
    try:
        starting_time = time()  # Start time for response time calculation
        
        logger.info("Making predictions...")
        data_dict = jsonable_encoder(data)
        data_df = pd.DataFrame([data_dict])
        result = model.predict(data_df)[0]
        
        # Labels for all metrics
        label = {"api": "/predict"}

        # Increase the counter
        counter.add(1, label)

        # Mark the end of the response
        ending_time = time()
        elapsed_time = ending_time - starting_time

        # Add histogram
        logger.info(f"Elapsed time: {elapsed_time} seconds")
        histogram.record(elapsed_time, label)

        if int(result) == 1:
            return {"Rain Tomorrow": "Yes"}
        else:
            return {"Rain Tomorrow": "No"}

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088)
