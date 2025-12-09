# Auth Service

Servicio de autenticación y autorización con JWT.

## Puerto: 8001

## Endpoints

- `POST /auth/register` - Registrar usuario
- `POST /auth/login` - Iniciar sesión
- `POST /auth/refresh` - Refrescar token
- `POST /auth/logout` - Cerrar sesión
- `GET /auth/verify` - Verificar token
- `POST /auth/reset-password` - Restablecer contraseña

## Ejecutar

```powershell
uvicorn app.main:app --reload --port 8001
```

## Documentación

http://localhost:8001/docs
