# Analytics Service

Microservicio para gestionar analíticas y estadísticas del sistema hotelero.

## Puerto
8008

## Endpoints

### Analytics
- `GET /analytics/dashboard` - Obtener estadísticas generales del dashboard
- `GET /analytics/rooms/occupancy` - Obtener datos de ocupación de habitaciones
- `GET /analytics/restaurant/bookings` - Obtener estadísticas de reservaciones del restaurante
- `GET /analytics/revenue` - Obtener datos de ingresos (daily/weekly/monthly)
- `GET /analytics/users/activity` - Obtener estadísticas de actividad de usuarios
- `GET /analytics/experiences/summary` - Obtener resumen de experiencias de usuarios

## Características

Este servicio NO usa base de datos. En su lugar:
- Consulta otros microservicios vía HTTP (en producción)
- Retorna datos mock/simulados para demostración
- Agrega y procesa información de múltiples fuentes

## Respuestas de Ejemplo

### Dashboard
```json
{
  "total_rooms": 50,
  "occupied_rooms": 35,
  "total_reservations": 127,
  "total_revenue": 45678.50,
  "active_users": 89,
  "restaurant_bookings": 234
}
```

### Room Occupancy
```json
[
  {
    "date": "2024-12-01",
    "total_rooms": 50,
    "occupied_rooms": 35,
    "occupancy_rate": 70.0,
    "revenue": 5250.0
  }
]
```

### Revenue
```json
{
  "period": "daily",
  "room_revenue": 7500.00,
  "restaurant_revenue": 3200.00,
  "total_revenue": 10700.00
}
```

## Ejecutar el servicio

```bash
cd analytics_service
uvicorn app.main:app --reload --port 8008
```

## Dependencias
- FastAPI
- Pydantic
- python-jose[cryptography]
- uvicorn
