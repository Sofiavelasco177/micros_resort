# Despliegue en Plataforma Cloud (Coolify, Railway, Render, etc.)

## Arquitectura de Microservicios

Este proyecto utiliza una arquitectura de microservicios con 9 servicios independientes:

1. **API Gateway** (Puerto 8000) - Punto de entrada principal
2. **Auth Service** (Puerto 8001) - Autenticación y autorización
3. **User Service** (Puerto 8002) - Gestión de usuarios
4. **Room Service** (Puerto 8003) - Gestión de habitaciones
5. **Room Reservation Service** (Puerto 8004) - Reservas de habitaciones
6. **Restaurant Service** (Puerto 8005) - Gestión de restaurantes
7. **Restaurant Reservation Service** (Puerto 8006) - Reservas de restaurantes
8. **Experience Service** (Puerto 8007) - Gestión de experiencias
9. **Analytics Service** (Puerto 8008) - Análisis y reportes

## Opciones de Despliegue

### Opción 1: Despliegue con Docker Compose (Recomendado)

Para plataformas que soportan docker-compose (como Coolify con docker-compose habilitado):

1. Asegúrate de que tu plataforma soporte docker-compose
2. Configura las variables de entorno desde el archivo `.env`
3. La plataforma ejecutará `docker-compose up -d`

**Configuración en Coolify:**
- Tipo: Docker Compose
- Archivo: `docker-compose.yml`
- Puerto principal: 8000 (API Gateway)

### Opción 2: Despliegue Solo API Gateway

Si tu plataforma solo permite un Dockerfile:

**⚠️ LIMITACIÓN:** Solo el API Gateway estará disponible. Los microservicios internos NO estarán disponibles a menos que los despliegues por separado.

**Configuración:**
- Usa el `Dockerfile` en la raíz
- Puerto: 8000
- Configurar variables de entorno para URLs de servicios externos

### Opción 3: Despliegue Multi-Servicio (Cada servicio por separado)

Desplegar cada servicio como una aplicación independiente:

#### Auth Service
```yaml
Dockerfile: auth_service/Dockerfile
Puerto: 8001
Variables de entorno:
  DATABASE_URL: <tu_db_url>
  SECRET_KEY: <tu_secret_key>
```

#### User Service
```yaml
Dockerfile: user_service/Dockerfile
Puerto: 8002
Variables de entorno:
  DATABASE_URL: <tu_db_url>
  AUTH_SERVICE_URL: <url_auth_service>
```

#### Room Service
```yaml
Dockerfile: room_service/Dockerfile
Puerto: 8003
Variables de entorno:
  DATABASE_URL: <tu_db_url>
  AUTH_SERVICE_URL: <url_auth_service>
```

*... y así para cada servicio*

#### API Gateway (Última)
```yaml
Dockerfile: api_gateway/Dockerfile
Puerto: 8000
Variables de entorno:
  AUTH_SERVICE_URL: <url_auth_service>
  USER_SERVICE_URL: <url_user_service>
  ROOM_SERVICE_URL: <url_room_service>
  ... (todas las URLs de servicios)
```

## Configuración para Coolify

### Método 1: Docker Compose (Recomendado)

1. Crear nuevo recurso → Docker Compose
2. Conectar repositorio: `Sofiavelasco177/micros_resort`
3. Branch: `main`
4. Archivo compose: `docker-compose.yml`
5. Variables de entorno:
   ```env
   SECRET_KEY=tu-clave-secreta-muy-segura-min-32-caracteres
   ```

### Método 2: Nixpacks (Un solo servicio)

Si Coolify está usando Nixpacks y solo quieres el API Gateway:

1. Crear nuevo recurso → Aplicación
2. Conectar repositorio
3. Build pack: Nixpacks o Docker
4. Puerto: 8000
5. Comando de inicio: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

**Modificar variables de entorno:**
```env
SECRET_KEY=tu-clave-secreta
AUTH_SERVICE_URL=https://auth.tudominio.com
USER_SERVICE_URL=https://user.tudominio.com
ROOM_SERVICE_URL=https://room.tudominio.com
ROOM_RESERVATION_SERVICE_URL=https://room-reservation.tudominio.com
RESTAURANT_SERVICE_URL=https://restaurant.tudominio.com
RESTAURANT_RESERVATION_SERVICE_URL=https://restaurant-reservation.tudominio.com
EXPERIENCE_SERVICE_URL=https://experience.tudominio.com
ANALYTICS_SERVICE_URL=https://analytics.tudominio.com
```

## Variables de Entorno Requeridas

Mínimas para API Gateway:
```env
SECRET_KEY=your-secret-key-minimum-32-characters
AUTH_SERVICE_URL=http://auth-service:8001
USER_SERVICE_URL=http://user-service:8002
ROOM_SERVICE_URL=http://room-service:8003
ROOM_RESERVATION_SERVICE_URL=http://room-reservation-service:8004
RESTAURANT_SERVICE_URL=http://restaurant-service:8005
RESTAURANT_RESERVATION_SERVICE_URL=http://restaurant-reservation-service:8006
EXPERIENCE_SERVICE_URL=http://experience-service:8007
ANALYTICS_SERVICE_URL=http://analytics-service:8008
```

Para cada servicio individual:
```env
DATABASE_URL=sqlite:///./data/<servicio>.db
SECRET_KEY=your-secret-key
AUTH_SERVICE_URL=<url_del_auth_service>
```

## Base de Datos

Por defecto, el proyecto usa **SQLite** (archivos locales). Para producción, considera:

1. **PostgreSQL** - Recomendado para producción
2. **MySQL/MariaDB** - Alternativa
3. **SQLite** - Solo para testing/desarrollo

## Problemas Comunes

### Error: "No module named 'app'"
- Verifica que el Dockerfile copie correctamente la carpeta `app`
- Revisa el contexto de build

### Error: "Cannot connect to service"
- Verifica que las URLs de servicios sean correctas
- En docker-compose, usa nombres de servicio (ej: `http://auth-service:8001`)
- En deployment separado, usa URLs públicas (ej: `https://auth.tudominio.com`)

### Error: Database connection
- Verifica que la variable `DATABASE_URL` esté configurada
- Asegúrate de que el directorio `/app/data` exista y tenga permisos

## Recomendación Final

Para un deployment exitoso en Coolify:

**MEJOR OPCIÓN:** Usar Docker Compose si tu instancia de Coolify lo soporta.

**SI NO:** Desplegar cada servicio individualmente y configurar las URLs de comunicación entre servicios.
