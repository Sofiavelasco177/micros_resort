# Guía de Despliegue con Docker

## Requisitos Previos
- Docker Desktop instalado y corriendo
- Docker Compose v3.8 o superior

## Configuración Inicial

1. **Copiar archivo de variables de entorno:**
   ```bash
   cp .env.example .env
   ```

2. **Editar el archivo .env y cambiar los valores:**
   - Especialmente el `SECRET_KEY` por uno seguro

## Comandos Docker

### Iniciar todos los servicios
```bash
docker-compose up -d
```

### Ver logs de todos los servicios
```bash
docker-compose logs -f
```

### Ver logs de un servicio específico
```bash
docker-compose logs -f auth-service
```

### Detener todos los servicios
```bash
docker-compose down
```

### Detener y eliminar volúmenes (datos)
```bash
docker-compose down -v
```

### Reconstruir las imágenes
```bash
docker-compose build
```

### Reconstruir y reiniciar
```bash
docker-compose up -d --build
```

### Ver estado de los servicios
```bash
docker-compose ps
```

## Acceso a los Servicios

Una vez desplegados, los servicios estarán disponibles en:

- **API Gateway:** http://localhost:8000/docs
- **Auth Service:** http://localhost:8001/docs
- **User Service:** http://localhost:8002/docs
- **Room Service:** http://localhost:8003/docs
- **Room Reservation Service:** http://localhost:8004/docs
- **Restaurant Service:** http://localhost:8005/docs
- **Restaurant Reservation Service:** http://localhost:8006/docs
- **Experience Service:** http://localhost:8007/docs
- **Analytics Service:** http://localhost:8008/docs

## Verificar Salud de los Servicios

```bash
# Verificar todos los contenedores
docker-compose ps

# Verificar salud del API Gateway
curl http://localhost:8000/health

# Verificar salud del Auth Service
curl http://localhost:8001/health
```

## Escalado de Servicios

Para escalar un servicio específico:
```bash
docker-compose up -d --scale room-service=3
```

## Troubleshooting

### Ver logs de errores
```bash
docker-compose logs --tail=100 [service-name]
```

### Reiniciar un servicio específico
```bash
docker-compose restart [service-name]
```

### Entrar a un contenedor
```bash
docker-compose exec [service-name] /bin/bash
```

### Limpiar todo (contenedores, imágenes, volúmenes)
```bash
docker-compose down -v --rmi all
```

## Persistencia de Datos

Los datos de las bases de datos SQLite se almacenan en volúmenes Docker:
- `auth-data`
- `user-data`
- `room-data`
- `room-reservation-data`
- `restaurant-data`
- `restaurant-reservation-data`
- `experience-data`
- `analytics-data`

Para hacer backup:
```bash
docker run --rm -v micros_resort_auth-data:/data -v $(pwd):/backup alpine tar czf /backup/auth-backup.tar.gz -C /data .
```

## Despliegue en Producción

### Consideraciones:
1. Cambiar SQLite por PostgreSQL o MySQL
2. Usar secretos de Docker para credenciales
3. Configurar reverse proxy (nginx/traefik)
4. Habilitar HTTPS
5. Configurar límites de recursos
6. Implementar logging centralizado
7. Configurar monitoring (Prometheus/Grafana)

### Ejemplo con PostgreSQL:
Modificar `docker-compose.yml` para agregar PostgreSQL:
```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_USER: resort_user
      POSTGRES_DB: resort_db
    volumes:
      - postgres-data:/var/lib/postgresql/data
```

Y actualizar las URLs de base de datos en variables de entorno.
