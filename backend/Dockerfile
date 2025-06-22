# Use official Python image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies and update CA certificates
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the backend app code
COPY ./app ./app

# Expose port FastAPI will run on
EXPOSE 8000

# Run the app with Uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
