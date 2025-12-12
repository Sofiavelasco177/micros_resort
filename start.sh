#!/bin/bash
set -e

echo "Starting API Gateway..."
echo "Port: ${PORT:-8000}"

# Si PORT está definido por Coolify, usarlo, sino usar 8000
export PORT=${PORT:-8000}

# Cambiar al directorio correcto
cd /code

# Iniciar aplicación
exec uvicorn api_gateway.app.main:app --host 0.0.0.0 --port $PORT
