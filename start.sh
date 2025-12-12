#!/bin/bash
set -e

echo "Starting API Gateway..."
echo "Port: ${PORT:-8000}"
echo "Current directory: $(pwd)"
echo "Python path: $PYTHONPATH"
echo "Listing files:"
ls -la

# Si PORT está definido por Coolify, usarlo, sino usar 8000
export PORT=${PORT:-8000}

# Iniciar aplicación
exec uvicorn api_gateway.app.main:app --host 0.0.0.0 --port $PORT
