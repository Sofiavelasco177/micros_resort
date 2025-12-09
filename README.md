# Sistema de Gestión Hotelera - Arquitectura de Microservicios

Sistema completo de gestión hotelera construido con arquitectura de microservicios usando FastAPI y SQLite.

## Servicios

| Servicio | Puerto | Descripción | Endpoints |
|----------|--------|-------------|-----------|
| API Gateway | 8000 | Punto de entrada único | - |
| Auth Service | 8001 | Autenticación y autorización | 6 |
| User Service | 8002 | Gestión de usuarios | 7 |
| Room Service | 8003 | Gestión de habitaciones | 10 |
| Room Reservation Service | 8004 | Reservas de habitaciones | 8 |
| Restaurant Service | 8005 | Gestión de restaurante | 10 |
| Restaurant Reservation Service | 8006 | Reservas de restaurante | 7 |
| Experience Service | 8007 | Reseñas y experiencias | 6 |
| Analytics Service | 8008 | Dashboard y estadísticas | 6 |

**Total: ~60 endpoints**
##  Inicio Rápido

### Instalación

```powershell
# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar todos los servicios

```powershell
# Opción 1: Ejecutar script de inicio
.\start_all_services.ps1

# Opción 2: Ejecutar cada servicio manualmente
# En terminales separadas:
cd auth_service ; uvicorn app.main:app --reload --port 8001
cd user_service ; uvicorn app.main:app --reload --port 8002
cd room_service ; uvicorn app.main:app --reload --port 8003
cd room_reservation_service ; uvicorn app.main:app --reload --port 8004
cd restaurant_service ; uvicorn app.main:app --reload --port 8005
cd restaurant_reservation_service ; uvicorn app.main:app --reload --port 8006
cd experience_service ; uvicorn app.main:app --reload --port 8007
cd analytics_service ; uvicorn app.main:app --reload --port 8008
cd api_gateway ; uvicorn app.main:app --reload --port 8000
```

### Acceder a la documentación

Una vez ejecutados los servicios:

- **API Gateway**: http://localhost:8000/docs
- **Auth Service**: http://localhost:8001/docs
- **User Service**: http://localhost:8002/docs
- **Room Service**: http://localhost:8003/docs
- **Room Reservation Service**: http://localhost:8004/docs
- **Restaurant Service**: http://localhost:8005/docs
- **Restaurant Reservation Service**: http://localhost:8006/docs
- **Experience Service**: http://localhost:8007/docs
- **Analytics Service**: http://localhost:8008/docs

## Autenticación

El sistema usa JWT para autenticación. Para usar los endpoints protegidos:

1. Registrarse o iniciar sesión en `/auth/login`
2. Usar el token en el header: `Authorization: Bearer <token>`

### Roles

- **user**: Usuario estándar (puede hacer reservas, crear experiencias)
- **admin**: Administrador (puede gestionar habitaciones, menú, ver todas las reservas)

## Estructura del Proyecto

```
micros_resort/
├── api_gateway/              # Puerto 8000
├── auth_service/             # Puerto 8001
├── user_service/             # Puerto 8002
├── room_service/             # Puerto 8003
├── room_reservation_service/ # Puerto 8004
├── restaurant_service/       # Puerto 8005
├── restaurant_reservation_service/ # Puerto 8006
├── experience_service/       # Puerto 8007
├── analytics_service/        # Puerto 8008
├── requirements.txt
├── .env
└── README.md
```

##  Stack Tecnológico

- **Framework**: FastAPI
- **Base de Datos**: SQLite (una por microservicio)
- **ORM**: SQLAlchemy
- **Validación**: Pydantic
- **Autenticación**: JWT
- **Comunicación**: REST API

##  Ejemplos de Uso

### Registrar un usuario

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "+34123456789"
  }'
```

### Hacer una reserva de habitación

```bash
curl -X POST http://localhost:8000/room_reservations/ \
  -H "Authorization: Bearer <tu-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": 1,
    "check_in_date": "2025-12-15",
    "check_out_date": "2025-12-20",
    "guests_count": 2,
    "special_requests": "Vista al mar"
  }'
```

##  Comunicación entre Servicios

Los servicios se comunican a través del API Gateway, que enruta las peticiones al microservicio correspondiente.

## Base de Datos

Cada microservicio tiene su propia base de datos SQLite:

- `auth_service/database.db`
- `user_service/database.db`
- `room_service/database.db`
- etc.

##  Testing

```powershell
# Ejecutar tests de un servicio específico
cd auth_service
pytest
```

##  Licencia

MIT

##  Contribución
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request
