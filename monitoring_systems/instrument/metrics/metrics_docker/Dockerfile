FROM python:3.8

WORKDIR /app

COPY requirements.txt /app
COPY metrics.py /app
COPY models /app/models
COPY date_transformer.py /app

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8099

CMD ["python", "metrics.py"]