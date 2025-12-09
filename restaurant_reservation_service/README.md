# Restaurant Reservation Service

Microservicio para gestionar reservaciones de mesas del restaurante en el sistema hotelero.

## Puerto
8006

## Endpoints

### Restaurant Reservations
- `GET /reservations/restaurant/` - Obtener todas las reservaciones (admin)
- `GET /reservations/restaurant/my` - Obtener reservaciones del usuario actual
- `GET /reservations/restaurant/{id}` - Obtener una reservación específica
- `POST /reservations/restaurant/` - Crear nueva reservación
- `PUT /reservations/restaurant/{id}` - Actualizar reservación
- `DELETE /reservations/restaurant/{id}` - Eliminar reservación
- `PATCH /reservations/restaurant/{id}/status` - Actualizar estado de reservación

## Modelo de Datos

### RestaurantReservation
- id: Integer (PK)
- user_id: Integer
- table_id: Integer
- reservation_date: Date
- reservation_time: Time
- guests_count: Integer
- status: String (pending, confirmed, cancelled, completed)
- special_requests: String (opcional)
- created_at: DateTime

## Ejecutar el servicio

```bash
cd restaurant_reservation_service
uvicorn app.main:app --reload --port 8006
```

## Dependencias
- FastAPI
- SQLAlchemy
- Pydantic
- python-jose[cryptography]
- passlib[bcrypt]
- uvicorn
