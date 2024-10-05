# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the necessary files
COPY models /app/models
COPY Notebooks /app/Notebooks
# COPY Notebooks/date_transformer.py /app/date_transformer.py
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set MODEL_PATH env variable
ENV MODEL_PATH /app/models/model.pkl

# Expose port 30000 for documentation purposes
EXPOSE 30000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]
