# Read more about OpenTelemetry here:
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
from io import BytesIO
import joblib
import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from pydantic import BaseModel
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Notebooks')))
from date_transformer import DateCyclicalTransformer


set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "rain-prediction-service"})
    )
)
tracer = get_tracer_provider().get_tracer("rain-prediction", "1.0.0")
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
get_tracer_provider().add_span_processor(span_processor)


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

# Initialize instance
app = FastAPI()


# Create an endpoint to check api work or not
@app.get("/")
def check_health():
    return {"status": "Oke"}


# Create an endpoint to make prediction
@app.post("/predict")
async def predict(data: WeatherFeatures):
    with tracer.start_as_current_span("processors") as processors:
        with tracer.start_as_current_span(
            "Prediction", links=[trace.Link(processors.get_span_context())]
        ):
            logger.info("Making predictions...")
            logger.info(data)
            logger.info(jsonable_encoder(data))
            logger.info(pd.DataFrame(jsonable_encoder(data), index=[0]))
            result = model.predict(pd.DataFrame(jsonable_encoder(data), index=[0]))[0]

    return {"result": ["Rain", "No Rain"][result]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8098)
