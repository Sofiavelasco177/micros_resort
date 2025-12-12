#!/bin/bash
set -e

echo "Starting API Gateway..."
echo "Port: ${PORT:-8000}"

# Si PORT está definido por Coolify, usarlo, sino usar 8000
export PORT=${PORT:-8000}

# Iniciar aplicación
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
