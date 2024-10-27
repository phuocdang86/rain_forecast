from time import sleep

import requests
from loguru import logger

json_data = {
    "Date": '2014-03-25',
    "Location":  'CoffsHarbour',
    "MinTemp": 17.5,
    "MaxTemp": 24.4,
    "Rainfall": 16.8,
    "Evaporation": 3.4,
    "Sunshine":  0.9,
    "WindGustDir": 'SE',
    "WindGustSpeed": 15.0,
    "WindDir9am": 'WSW',
    "WindDir3pm": 'SE',
    "WindSpeed9am": 7.0,
    "WindSpeed3pm":  9.0,
    "Humidity9am":  89.0,
    "Humidity3pm": 73.0,
    "Pressure9am": 1019.0,
    "Pressure3pm": 1018.7,
    "Cloud9am" : 7.0,
    "Cloud3pm" :  8.0,
    "Temp9am" : 20.5,
    "Temp3pm" :  23.8,
    "RainToday" : 'Yes'
}


def predict():
    logger.info("Sending POST requests!")
    response = requests.post(
        "http://localhost:8088/predict",
        headers={
            "accept": "application/json",
        },
        json=json_data,
    )


if __name__ == "__main__":
    while True:
        predict()
        sleep(1)
