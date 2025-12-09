# API Examples - Hotel Management System

Colección de ejemplos de uso de la API del sistema hotelero.

## Variables de Entorno

```bash
API_BASE_URL=http://localhost:8000
TOKEN=<tu-token-jwt>
```

## 🔐 Autenticación

### Registrarse

```bash
curl -X POST $API_BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "+123456789"
  }'
```

### Iniciar Sesión

```bash
curl -X POST $API_BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

Respuesta:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## 🏠 Habitaciones

### Listar Habitaciones Disponibles

```bash
curl -X GET "$API_BASE_URL/rooms/available?room_type=suite"
```

### Obtener Detalles de Habitación

```bash
curl -X GET $API_BASE_URL/rooms/1
```

### Crear Habitación (Admin)

```bash
curl -X POST $API_BASE_URL/rooms/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "room_number": "501",
    "type": "suite",
    "price_per_night": 150,
    "capacity": 4,
    "description": "Suite con vista al mar",
    "amenities": ["wifi", "tv", "minibar", "balcony", "ocean_view"]
  }'
```

## 📅 Reservas de Habitaciones

### Verificar Disponibilidad

```bash
curl -X GET "$API_BASE_URL/reservations/rooms/check-availability?room_id=1&check_in=2025-12-15&check_out=2025-12-20"
```

### Crear Reserva

```bash
curl -X POST $API_BASE_URL/reservations/rooms/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": 1,
    "check_in_date": "2025-12-15",
    "check_out_date": "2025-12-20",
    "guests_count": 2,
    "special_requests": "Habitación en piso alto, vista al mar"
  }'
```

### Ver Mis Reservas

```bash
curl -X GET $API_BASE_URL/reservations/rooms/my \
  -H "Authorization: Bearer $TOKEN"
```

### Cancelar Reserva

```bash
curl -X DELETE $API_BASE_URL/reservations/rooms/1 \
  -H "Authorization: Bearer $TOKEN"
```

## 🍽️ Restaurante

### Ver Menú

```bash
curl -X GET $API_BASE_URL/restaurant/menu/
```

### Filtrar por Categoría

```bash
curl -X GET "$API_BASE_URL/restaurant/menu/?category=main"
```

### Crear Item de Menú (Admin)

```bash
curl -X POST $API_BASE_URL/restaurant/menu/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pasta Carbonara",
    "description": "Pasta italiana con salsa cremosa",
    "category": "main",
    "price": 18.50,
    "allergens": ["gluten", "dairy", "eggs"]
  }'
```

### Ver Mesas Disponibles

```bash
curl -X GET $API_BASE_URL/restaurant/tables/
```

## 📅 Reservas de Restaurante

### Crear Reserva de Mesa

```bash
curl -X POST $API_BASE_URL/restaurant_reservations/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "table_id": 1,
    "reservation_date": "2025-12-15",
    "reservation_time": "20:00:00",
    "guests_count": 4,
    "special_requests": "Mesa junto a la ventana"
  }'
```

### Ver Mis Reservas de Restaurante

```bash
curl -X GET $API_BASE_URL/restaurant_reservations/my \
  -H "Authorization: Bearer $TOKEN"
```

## ⭐ Experiencias

### Publicar Experiencia

```bash
curl -X POST $API_BASE_URL/experiences/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Excelente estadía",
    "content": "Las instalaciones son magníficas y el personal muy atento",
    "rating": 5,
    "category": "service"
  }'
```

### Ver Experiencias Públicas

```bash
curl -X GET $API_BASE_URL/experiences/public
```

## 📊 Analytics (Admin)

### Dashboard General

```bash
curl -X GET $API_BASE_URL/analytics/dashboard \
  -H "Authorization: Bearer $TOKEN"
```

### Ocupación de Habitaciones

```bash
curl -X GET $API_BASE_URL/analytics/rooms/occupancy \
  -H "Authorization: Bearer $TOKEN"
```

### Ingresos

```bash
curl -X GET $API_BASE_URL/analytics/revenue \
  -H "Authorization: Bearer $TOKEN"
```

## 👤 Gestión de Usuario

### Ver Mi Perfil

```bash
curl -X GET $API_BASE_URL/users/profile/me \
  -H "Authorization: Bearer $TOKEN"
```

### Actualizar Perfil

```bash
curl -X PUT $API_BASE_URL/users/profile/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan Carlos",
    "phone": "+123456789"
  }'
```

## 🔄 Flujo Completo de Ejemplo

### 1. Usuario se registra
### 2. Busca habitaciones disponibles
### 3. Hace una reserva de habitación
### 4. Reserva mesa en restaurante
### 5. Después de su estadía, deja una reseña

```bash
# 1. Registrarse
TOKEN=$(curl -X POST $API_BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"guest@example.com","password":"pass123","first_name":"Guest","last_name":"User"}' \
  | jq -r '.access_token')

# 2. Ver habitaciones
curl -X GET $API_BASE_URL/rooms/available

# 3. Hacer reserva
curl -X POST $API_BASE_URL/reservations/rooms/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"room_id":1,"check_in_date":"2025-12-15","check_out_date":"2025-12-20","guests_count":2}'

# 4. Reservar mesa
curl -X POST $API_BASE_URL/restaurant_reservations/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"table_id":1,"reservation_date":"2025-12-15","reservation_time":"20:00:00","guests_count":2}'

# 5. Dejar reseña
curl -X POST $API_BASE_URL/experiences/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Gran experiencia","content":"Todo perfecto","rating":5,"category":"service"}'
```

## 🔍 Tips

- Todos los endpoints están documentados en: `http://localhost:8000/docs`
- Usa la interfaz Swagger para probar endpoints interactivamente
- El token JWT expira en 30 minutos (renovable con el refresh token)
- Los endpoints de admin requieren que el usuario tenga `role: "admin"`

## 📱 Códigos de Estado HTTP

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error
