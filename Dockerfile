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

# Upgrade pip and install PyTorch with CUDA support
RUN pip3 install --upgrade pip && \
    pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu113

# Set working directory
WORKDIR /app

# Copy application code
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy model weights
COPY weights/RealESRGAN_x4plus.pth /app/weights/

COPY . .

# Expose the port your app will run on (default: 5000)
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
