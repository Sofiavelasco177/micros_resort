# Room Reservation Service

Microservicio para gestionar reservaciones de habitaciones en el sistema hotelero.

## Puerto
8004

## Endpoints

### Room Reservations
- `GET /reservations/rooms/` - Obtener todas las reservaciones (admin)
- `GET /reservations/rooms/my` - Obtener reservaciones del usuario actual
- `GET /reservations/rooms/{id}` - Obtener una reservación específica
- `POST /reservations/rooms/` - Crear nueva reservación
- `PUT /reservations/rooms/{id}` - Actualizar reservación
- `DELETE /reservations/rooms/{id}` - Eliminar reservación
- `PATCH /reservations/rooms/{id}/status` - Actualizar estado de reservación
- `GET /reservations/rooms/check-availability` - Verificar disponibilidad

## Modelo de Datos

### RoomReservation
- id: Integer (PK)
- user_id: Integer
- room_id: Integer
- check_in_date: Date
- check_out_date: Date
- guests_count: Integer
- total_price: Float
- status: String (pending, confirmed, cancelled, completed)
- special_requests: String (opcional)
- created_at: DateTime

## Ejecutar el servicio

```bash
cd room_reservation_service
uvicorn app.main:app --reload --port 8004
```

## Dependencias
- FastAPI
- SQLAlchemy
- Pydantic
- python-jose[cryptography]
- passlib[bcrypt]
- uvicorn
