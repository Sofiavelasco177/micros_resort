# 🏗️ Arquitectura del Sistema

## Diagrama de Arquitectura

```
                    ┌─────────────────────────────────────────┐
                    │         CLIENTE / FRONTEND              │
                    │    (Web Browser / Mobile App / API)     │
                    └────────────────┬────────────────────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────────────────┐
                    │         API GATEWAY (Puerto 8000)       │
                    │  - Enrutamiento                         │
                    │  - Validación de tokens                 │
                    │  - Rate limiting                        │
                    │  - Logging                              │
                    └────────────────┬────────────────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        ▼                            ▼                            ▼
┌───────────────┐          ┌────────────────┐          ┌────────────────┐
│  Auth Service │          │  User Service  │          │  Room Service  │
│   (Port 8001) │          │  (Port 8002)   │          │  (Port 8003)   │
│               │          │                │          │                │
│ - Register    │          │ - CRUD Users   │          │ - CRUD Rooms   │
│ - Login       │◄─────────┤ - Profiles     │          │ - Inventory    │
│ - Tokens      │          │ - Roles        │          │ - Availability │
│ - Verify      │          │                │          │                │
└───────┬───────┘          └────────────────┘          └────────────────┘
        │                           │                           │
        │                           │                           │
    [SQLite]                    [SQLite]                   [SQLite]
  auth_tokens                    users                       rooms
                                                        room_inventory

        │                            │                            │
        ▼                            ▼                            ▼
┌───────────────────┐     ┌────────────────────┐     ┌────────────────────┐
│ Room Reservation  │     │ Restaurant Service │     │Restaurant Reserv.  │
│   (Port 8004)     │     │    (Port 8005)     │     │   (Port 8006)      │
│                   │     │                    │     │                    │
│ - Book rooms      │     │ - Menu items       │     │ - Book tables      │
│ - Check-in/out    │     │ - Tables           │     │ - Manage bookings  │
│ - Manage bookings │     │ - Availability     │     │ - Special requests │
└─────────┬─────────┘     └──────────┬─────────┘     └──────────┬─────────┘
          │                          │                           │
      [SQLite]                   [SQLite]                    [SQLite]
  room_reservations          menu_items                restaurant_reserv
                        restaurant_tables

        │                            │
        ▼                            ▼
┌───────────────────┐       ┌────────────────────┐
│Experience Service │       │ Analytics Service  │
│   (Port 8007)     │       │    (Port 8008)     │
│                   │       │                    │
│ - Reviews         │       │ - Dashboard        │
│ - Ratings         │       │ - Occupancy stats  │
│ - Public/Private  │       │ - Revenue reports  │
└─────────┬─────────┘       │ - User activity    │
          │                 └────────────────────┘
      [SQLite]                       │
    experiences              (Consulta otros servicios)
```

## 🔄 Flujo de Comunicación

### Autenticación
```
1. Cliente → API Gateway → Auth Service → User Service
2. User Service valida credenciales
3. Auth Service genera JWT token
4. Token se retorna al cliente
```

### Crear Reserva (Ejemplo)
```
1. Cliente envía petición con JWT token
2. API Gateway valida token con Auth Service
3. Gateway enruta a Room Reservation Service
4. Room Reservation consulta Room Service (disponibilidad)
5. Se crea la reserva en la BD del servicio
6. Respuesta fluye de vuelta al cliente
```

## 📦 Componentes por Capa

### Capa de Presentación
- **API Gateway** (FastAPI)
  - Punto de entrada único
  - Enrutamiento inteligente
  - Validación de autenticación
  - Manejo de errores centralizado

### Capa de Servicios (Microservicios)

#### Autenticación y Usuarios
- **Auth Service**: JWT tokens, login, register
- **User Service**: Gestión de usuarios y perfiles

#### Gestión Hotelera
- **Room Service**: Habitaciones e inventario
- **Room Reservation Service**: Reservas de habitaciones

#### Restaurante
- **Restaurant Service**: Menú y mesas
- **Restaurant Reservation Service**: Reservas de restaurante

#### Complementarios
- **Experience Service**: Reseñas y experiencias
- **Analytics Service**: Estadísticas y dashboard

### Capa de Datos
- Cada microservicio tiene su propia base de datos SQLite
- Independencia de datos (no comparten tablas)
- Comunicación vía API REST

## 🔐 Seguridad

### Autenticación
- JWT (JSON Web Tokens)
- Access token (30 min)
- Refresh token (7 días)

### Autorización
- Roles: `user`, `admin`
- Validación en cada endpoint protegido
- Middleware de autenticación en cada servicio

### Comunicación
- HTTPS recomendado en producción
- CORS configurado
- Headers de seguridad

## 🗄️ Bases de Datos

Cada servicio mantiene su propia base de datos:

| Servicio | Base de Datos | Tablas |
|----------|---------------|--------|
| Auth | `auth_service/database.db` | auth_tokens |
| User | `user_service/database.db` | users |
| Room | `room_service/database.db` | rooms, room_inventory |
| Room Reservation | `room_reservation_service/database.db` | room_reservations |
| Restaurant | `restaurant_service/database.db` | menu_items, restaurant_tables |
| Restaurant Reservation | `restaurant_reservation_service/database.db` | restaurant_reservations |
| Experience | `experience_service/database.db` | experiences |
| Analytics | N/A | (consulta otros servicios) |

## 🔄 Patrones de Diseño Utilizados

### API Gateway Pattern
- Punto de entrada único
- Enrutamiento centralizado
- Autenticación en el gateway

### Database per Service
- Cada microservicio tiene su BD
- Independencia y aislamiento
- Escalabilidad independiente

### Service Registry Pattern (Implícito)
- Configuración de URLs de servicios
- Verificación de salud de servicios

### Circuit Breaker Pattern (Recomendado para producción)
- Manejo de fallos de servicios
- Timeouts configurados

## 📈 Escalabilidad

### Vertical
Cada servicio puede escalar independientemente:
- Más CPU/RAM según demanda
- Optimización de queries

### Horizontal
- Múltiples instancias del mismo servicio
- Load balancer delante del API Gateway
- Base de datos puede migrar a PostgreSQL/MySQL

### Recomendaciones para Producción

1. **Containerización**: Usar Docker
2. **Orquestación**: Kubernetes o Docker Swarm
3. **Base de datos**: PostgreSQL o MySQL en lugar de SQLite
4. **Cache**: Redis para tokens y datos frecuentes
5. **Message Queue**: RabbitMQ o Kafka para comunicación asíncrona
6. **Monitoring**: Prometheus + Grafana
7. **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

## 🚀 Despliegue

### Desarrollo (Actual)
- Todos los servicios en localhost
- Puertos 8000-8008
- SQLite como base de datos

### Staging/Producción (Recomendado)
```
┌─────────────────────────────────────┐
│     Load Balancer (Nginx/AWS)      │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│     API Gateway Cluster (3x)        │
└────────────┬────────────────────────┘
             │
┌────────────┴────────────────────────┐
│   Microservices (Kubernetes Pods)   │
│   - Auto-scaling                    │
│   - Health checks                   │
│   - Rolling updates                 │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Database Cluster (PostgreSQL)     │
│   - Replication                     │
│   - Backups                         │
└─────────────────────────────────────┘
```

## 🔍 Monitoreo y Observabilidad

### Health Checks
- Cada servicio expone `/health`
- API Gateway consulta estado de servicios
- Script `check_services.ps1`

### Logging
- Logs en stdout/stderr
- Niveles: INFO, WARNING, ERROR
- Formato estructurado (JSON recomendado)

### Métricas (Recomendado)
- Request count
- Response time
- Error rate
- Database query time

## 🧪 Testing

### Tipos de Tests Recomendados

1. **Unit Tests**: Para lógica de negocio en services
2. **Integration Tests**: Para endpoints completos
3. **E2E Tests**: Flujos completos a través del gateway
4. **Load Tests**: Capacidad y rendimiento

### Ejemplo de Test
```python
def test_create_room():
    response = client.post("/rooms/", 
        json={"room_number": "101", "type": "single", ...},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
```

## 📚 Referencias

- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- JWT: https://jwt.io/
- Microservices Pattern: https://microservices.io/
