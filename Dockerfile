# Dockerfile principal para despliegue del API Gateway
FROM python:3.12-slim

# Set working directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire api_gateway directory
COPY api_gateway ./api_gateway

# Copy startup script
COPY start.sh .
RUN chmod +x start.sh

# Set Python path to find modules
ENV PYTHONPATH=/code

# Expose port
EXPOSE 8000

# Run the application
CMD ["bash", "start.sh"]
