# Experience Service

Microservicio para gestionar experiencias y reseñas de usuarios en el sistema hotelero.

## Puerto
8007

## Endpoints

### Experiences
- `GET /experiences/` - Obtener todas las experiencias (admin)
- `GET /experiences/public` - Obtener experiencias públicas (sin autenticación)
- `GET /experiences/{id}` - Obtener una experiencia específica
- `POST /experiences/` - Crear nueva experiencia
- `PUT /experiences/{id}` - Actualizar experiencia
- `DELETE /experiences/{id}` - Eliminar experiencia

## Modelo de Datos

### Experience
- id: Integer (PK)
- user_id: Integer
- title: String
- content: String
- rating: Integer (1-5)
- category: String (accommodation, restaurant, spa, activities, general)
- is_public: Boolean
- created_at: DateTime

## Ejecutar el servicio

```bash
cd experience_service
uvicorn app.main:app --reload --port 8007
```

## Dependencias
- FastAPI
- SQLAlchemy
- Pydantic
- python-jose[cryptography]
- passlib[bcrypt]
- uvicorn
