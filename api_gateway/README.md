# API Gateway

Punto de entrada único para todos los microservicios del sistema hotelero.

## Puerto: 8000

## Funciones

- **Enrutamiento**: Dirige las peticiones al microservicio correspondiente
- **Monitoreo**: Verifica el estado de todos los servicios
- **CORS**: Configurado para aceptar peticiones desde cualquier origen
- **Logging**: Registra todas las peticiones y respuestas

## Servicios Disponibles

| Ruta | Servicio | Puerto |
|------|----------|--------|
| `/auth/*` | Auth Service | 8001 |
| `/users/*` | User Service | 8002 |
| `/rooms/*` | Room Service | 8003 |
| `/reservations/rooms/*` | Room Reservation Service | 8004 |
| `/restaurant/*` | Restaurant Service | 8005 |
| `/restaurant_reservations/*` | Restaurant Reservation Service | 8006 |
| `/experiences/*` | Experience Service | 8007 |
| `/analytics/*` | Analytics Service | 8008 |

## Endpoints del Gateway

- `GET /` - Información del gateway
- `GET /health` - Health check
- `GET /services/status` - Estado de todos los microservicios
- `* /{service}/{path}` - Proxy a microservicios

## Uso

### Verificar estado de servicios

```bash
curl http://localhost:8000/services/status
```

### Hacer login (a través del gateway)

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Listar habitaciones disponibles

```bash
curl http://localhost:8000/rooms/available
```

### Crear reserva (con autenticación)

```bash
curl -X POST http://localhost:8000/reservations/rooms/ \
  -H "Authorization: Bearer <tu-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": 1,
    "check_in_date": "2025-12-15",
    "check_out_date": "2025-12-20",
    "guests_count": 2
  }'
```

## Ejecutar

```powershell
uvicorn app.main:app --reload --port 8000
```

## Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Características

- ✅ Enrutamiento automático a microservicios
- ✅ Manejo de errores (404, 503, 504, 500)
- ✅ Timeout de 30 segundos por petición
- ✅ Headers forwarding
- ✅ Query parameters forwarding
- ✅ Logging de peticiones
- ✅ CORS habilitado
- ✅ Monitoreo de servicios

## Notas

⚠️ **Importante**: Todos los microservicios deben estar ejecutándose para que el gateway funcione correctamente.

Para iniciar todos los servicios, usa el script `start_all_services.ps1` en la raíz del proyecto.
