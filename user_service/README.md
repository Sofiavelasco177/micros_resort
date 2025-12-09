# User Service

Servicio de gestión de usuarios y perfiles.

## Puerto: 8002

## Endpoints

- `GET /users/` - Listar usuarios (admin)
- `GET /users/{id}` - Obtener usuario
- `POST /users/` - Crear usuario (admin)
- `PUT /users/{id}` - Actualizar usuario
- `DELETE /users/{id}` - Eliminar usuario (admin)
- `GET /users/profile/me` - Ver perfil propio
- `PUT /users/profile/me` - Actualizar perfil propio

## Ejecutar

```powershell
uvicorn app.main:app --reload --port 8002
```

## Documentación

http://localhost:8002/docs
