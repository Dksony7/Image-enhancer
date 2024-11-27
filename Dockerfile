# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    curl \
    ca-certificates \
    libjpeg-dev \
    zlib1g-dev \
    libopenblas-dev \
    libopenmpi-dev && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port your app runs on (default Gunicorn port: 8000)
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "4"]
