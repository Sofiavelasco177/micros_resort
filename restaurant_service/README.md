# Restaurant Service

Microservicio para gestionar el menú y mesas del restaurante en el sistema hotelero.

## Puerto
8005

## Endpoints

### Menu Items
- `GET /menu` - Obtener todos los items del menú
- `GET /menu/{id}` - Obtener un item específico del menú
- `POST /menu` - Crear nuevo item del menú (admin)
- `PUT /menu/{id}` - Actualizar item del menú (admin)
- `DELETE /menu/{id}` - Eliminar item del menú (admin)

### Restaurant Tables
- `GET /tables` - Obtener todas las mesas
- `GET /tables/{id}` - Obtener una mesa específica
- `POST /tables` - Crear nueva mesa (admin)
- `PUT /tables/{id}` - Actualizar mesa (admin)
- `DELETE /tables/{id}` - Eliminar mesa (admin)

## Modelos de Datos

### MenuItem
- id: Integer (PK)
- name: String
- description: String (opcional)
- category: String (appetizer, main, dessert, beverage)
- price: Float
- is_available: Boolean
- image_url: String (opcional)
- allergens: JSON (lista de alérgenos)

### RestaurantTable
- id: Integer (PK)
- table_number: Integer (único)
- capacity: Integer
- location: String (indoor, outdoor, terrace)
- is_available: Boolean

## Ejecutar el servicio

```bash
cd restaurant_service
uvicorn app.main:app --reload --port 8005
```

## Dependencias
- FastAPI
- SQLAlchemy
- Pydantic
- python-jose[cryptography]
- passlib[bcrypt]
- uvicorn
