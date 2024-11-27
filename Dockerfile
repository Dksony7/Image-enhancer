FROM nvidia/cuda:11.3.1-base-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install Python and required dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python packages
RUN pip3 install --upgrade pip

# Set working directory
WORKDIR /app

# Copy application code
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

# Expose application port and set CMD
EXPOSE 8000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "4"]
