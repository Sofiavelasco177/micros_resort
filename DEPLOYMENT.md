# 🚀 Guía de Despliegue

Guía completa para desplegar el sistema de gestión hotelera en diferentes entornos.

## 📋 Contenido

1. [Requisitos](#requisitos)
2. [Desarrollo Local](#desarrollo-local)
3. [Despliegue con Docker](#despliegue-con-docker)
4. [Despliegue en la Nube](#despliegue-en-la-nube)
5. [Variables de Entorno](#variables-de-entorno)
6. [Seguridad](#seguridad)
7. [Monitoreo](#monitoreo)

---

## 📦 Requisitos

### Mínimos
- Python 3.9+
- 2GB RAM
- 5GB espacio en disco

### Recomendados para Producción
- Python 3.11+
- 4GB+ RAM
- 20GB+ espacio en disco
- PostgreSQL 14+ (en lugar de SQLite)
- Redis (para cache)
- Nginx (como reverse proxy)

---

## 💻 Desarrollo Local

### Opción 1: Ejecución Directa

```powershell
# 1. Clonar/descargar el proyecto
cd micros_resort

# 2. Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar todos los servicios
.\start_all_services.ps1

# 5. Configurar datos de prueba
.\setup_test_data.ps1
```

### Opción 2: Ejecutar Servicios Individualmente

```powershell
# Terminal 1 - Auth Service
cd auth_service
uvicorn app.main:app --reload --port 8001

# Terminal 2 - User Service
cd user_service
uvicorn app.main:app --reload --port 8002

# ... y así sucesivamente
```

---

## 🐳 Despliegue con Docker

### Paso 1: Crear Dockerfile para cada servicio

Ejemplo `Dockerfile` (crear uno en cada carpeta de servicio):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del servicio
COPY app/ ./app/

# Puerto expuesto (varía según servicio)
EXPOSE 8001

# Comando para ejecutar
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Paso 2: Crear docker-compose.yml

```yaml
version: '3.8'

services:
  auth-service:
    build: ./auth_service
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=sqlite:///./database.db
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - auth-data:/app

  user-service:
    build: ./user_service
    ports:
      - "8002:8002"
    environment:
      - DATABASE_URL=sqlite:///./database.db
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - user-data:/app

  room-service:
    build: ./room_service
    ports:
      - "8003:8003"
    environment:
      - DATABASE_URL=sqlite:///./database.db
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - room-data:/app

  room-reservation-service:
    build: ./room_reservation_service
    ports:
      - "8004:8004"
    environment:
      - DATABASE_URL=sqlite:///./database.db
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - room-reservation-data:/app

  restaurant-service:
    build: ./restaurant_service
    ports:
      - "8005:8005"
    environment:
      - DATABASE_URL=sqlite:///./database.db
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - restaurant-data:/app

  restaurant-reservation-service:
    build: ./restaurant_reservation_service
    ports:
      - "8006:8006"
    environment:
      - DATABASE_URL=sqlite:///./database.db
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - restaurant-reservation-data:/app

  experience-service:
    build: ./experience_service
    ports:
      - "8007:8007"
    environment:
      - DATABASE_URL=sqlite:///./database.db
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - experience-data:/app

  analytics-service:
    build: ./analytics_service
    ports:
      - "8008:8008"
    environment:
      - SECRET_KEY=${SECRET_KEY}

  api-gateway:
    build: ./api_gateway
    ports:
      - "8000:8000"
    environment:
      - AUTH_SERVICE_URL=http://auth-service:8001
      - USER_SERVICE_URL=http://user-service:8002
      - ROOM_SERVICE_URL=http://room-service:8003
      - ROOM_RESERVATION_SERVICE_URL=http://room-reservation-service:8004
      - RESTAURANT_SERVICE_URL=http://restaurant-service:8005
      - RESTAURANT_RESERVATION_SERVICE_URL=http://restaurant-reservation-service:8006
      - EXPERIENCE_SERVICE_URL=http://experience-service:8007
      - ANALYTICS_SERVICE_URL=http://analytics-service:8008
    depends_on:
      - auth-service
      - user-service
      - room-service
      - room-reservation-service
      - restaurant-service
      - restaurant-reservation-service
      - experience-service
      - analytics-service

volumes:
  auth-data:
  user-data:
  room-data:
  room-reservation-data:
  restaurant-data:
  restaurant-reservation-data:
  experience-data:
```

### Paso 3: Ejecutar con Docker Compose

```bash
# Construir imágenes
docker-compose build

# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

---

## ☁️ Despliegue en la Nube

### AWS (Elastic Beanstalk / ECS)

#### Opción 1: Elastic Beanstalk

```bash
# Instalar AWS CLI y EB CLI
pip install awsebcli

# Inicializar
eb init -p python-3.11 hotel-management

# Crear ambiente
eb create hotel-management-prod

# Desplegar
eb deploy

# Abrir en navegador
eb open
```

#### Opción 2: ECS (Elastic Container Service)

1. Subir imágenes a ECR (Elastic Container Registry)
2. Crear Task Definitions para cada servicio
3. Configurar ECS Cluster
4. Crear Services en el cluster
5. Configurar Application Load Balancer

### Google Cloud Platform (Cloud Run)

```bash
# Para cada servicio
gcloud run deploy auth-service \
  --source ./auth_service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# API Gateway
gcloud run deploy api-gateway \
  --source ./api_gateway \
  --platform managed \
  --region us-central1 \
  --set-env-vars AUTH_SERVICE_URL=https://auth-service-xxx.run.app
```

### Azure (App Service / Container Instances)

```bash
# Crear resource group
az group create --name hotel-rg --location eastus

# Crear container registry
az acr create --resource-group hotel-rg --name hotelregistry --sku Basic

# Construir y subir imágenes
az acr build --registry hotelregistry --image auth-service:v1 ./auth_service

# Crear container instances
az container create \
  --resource-group hotel-rg \
  --name auth-service \
  --image hotelregistry.azurecr.io/auth-service:v1 \
  --ports 8001
```

### Heroku

```bash
# Para cada servicio
cd auth_service
heroku create hotel-auth-service
git push heroku main

# Configurar variables
heroku config:set SECRET_KEY=tu-clave-secreta
```

---

## 🔐 Variables de Entorno

### Archivo .env para Producción

```bash
# JWT
SECRET_KEY=genera-una-clave-muy-segura-aqui-usar-secrets-generator
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Base de Datos (PostgreSQL en producción)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Services URLs (en producción usar dominios reales)
AUTH_SERVICE_URL=https://auth.tuhotel.com
USER_SERVICE_URL=https://users.tuhotel.com
ROOM_SERVICE_URL=https://rooms.tuhotel.com
# ... etc

# Redis (opcional, para cache)
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO

# CORS
ALLOWED_ORIGINS=https://tuhotel.com,https://www.tuhotel.com

# Email (para notificaciones)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-password
```

### Generar SECRET_KEY Seguro

```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 🛡️ Seguridad

### Checklist de Seguridad

- [ ] Cambiar `SECRET_KEY` por uno generado aleatoriamente
- [ ] Usar HTTPS en producción
- [ ] Configurar CORS apropiadamente (no usar `allow_origins=["*"]`)
- [ ] Migrar de SQLite a PostgreSQL
- [ ] Implementar rate limiting en API Gateway
- [ ] Agregar validación de entrada robusta
- [ ] Configurar logs sin exponer información sensible
- [ ] Usar variables de entorno para secrets (no hardcodear)
- [ ] Implementar backups automáticos de base de datos
- [ ] Configurar SSL/TLS en base de datos
- [ ] Auditar dependencias regularmente (`pip audit`)
- [ ] Implementar 2FA para usuarios admin

### Nginx como Reverse Proxy

```nginx
server {
    listen 80;
    server_name tuhotel.com;

    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name tuhotel.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # API Gateway
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20;
}
```

---

## 📊 Monitoreo

### Health Checks Automáticos

Crear script de monitoreo:

```bash
#!/bin/bash
# monitor.sh

services=(
  "http://localhost:8000/health"
  "http://localhost:8001/health"
  "http://localhost:8002/health"
  # ... etc
)

for service in "${services[@]}"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" $service)
  if [ $status -ne 200 ]; then
    echo "ALERT: Service $service is down (Status: $status)"
    # Enviar notificación (email, Slack, etc.)
  fi
done
```

### Prometheus + Grafana (Recomendado)

Agregar métricas a cada servicio:

```python
# requirements.txt
prometheus-fastapi-instrumentator==5.9.1

# En main.py
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)
```

### Logging Centralizado

Usar ELK Stack o servicio cloud (CloudWatch, Stackdriver, etc.)

---

## 🔄 CI/CD

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to AWS
        run: |
          # Comandos de despliegue
```

---

## 📞 Soporte

Para problemas de despliegue:
1. Revisar logs: `docker-compose logs [service-name]`
2. Verificar health checks: `./check_services.ps1`
3. Consultar documentación de la plataforma cloud específica

## 🔗 Referencias

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS ECS Guide](https://docs.aws.amazon.com/ecs/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
