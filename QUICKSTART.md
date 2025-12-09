# 🏨 Sistema de Gestión Hotelera - Guía Rápida

## ⚡ Inicio Rápido (3 pasos)

### 1. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 2. Iniciar todos los servicios

```powershell
.\start_all_services.ps1
```

Este script iniciará automáticamente los 9 microservicios en ventanas separadas.

### 3. Configurar datos de prueba

```powershell
.\setup_test_data.ps1
```

Esto creará:
- Usuario admin (admin@hotel.com / admin123)
- 4 habitaciones de ejemplo
- Menú del restaurante
- Mesas del restaurante

## 🌐 Acceso Rápido

- **API Gateway (punto de entrada)**: http://localhost:8000/docs
- **Verificar estado de servicios**: http://localhost:8000/services/status

## 📝 Ejemplo de Uso

### 1. Registrarse

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

### 2. Hacer una reserva

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

### 3. Ver habitaciones disponibles

```bash
curl http://localhost:8000/rooms/available
```

## 🛠️ Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `start_all_services.ps1` | Inicia todos los microservicios |
| `stop_all_services.ps1` | Detiene todos los servicios |
| `check_services.ps1` | Verifica el estado de los servicios |
| `setup_test_data.ps1` | Crea datos de prueba |

## 📊 Arquitectura

```
API Gateway (8000)
    │
    ├─► Auth Service (8001)
    ├─► User Service (8002)
    ├─► Room Service (8003)
    ├─► Room Reservation Service (8004)
    ├─► Restaurant Service (8005)
    ├─► Restaurant Reservation Service (8006)
    ├─► Experience Service (8007)
    └─► Analytics Service (8008)
```

## 🔐 Autenticación

Todos los endpoints protegidos requieren un token JWT en el header:

```
Authorization: Bearer <tu-token-aqui>
```

Obtén tu token en `/auth/login` o `/auth/register`.

## 📚 Documentación Completa

Ver [README.md](README.md) para documentación detallada.

## ❓ Problemas Comunes

### Los servicios no inician

```powershell
# Verifica que Python está instalado
python --version

# Verifica que las dependencias están instaladas
pip list
```

### Puertos ocupados

```powershell
# Detén todos los servicios
.\stop_all_services.ps1

# Luego inicia de nuevo
.\start_all_services.ps1
```

### Error de conexión entre servicios

Asegúrate de que todos los servicios están ejecutándose:

```powershell
.\check_services.ps1
```

## 💡 Tips

- Usa el **API Gateway** (puerto 8000) para todas las peticiones
- Cada servicio tiene su documentación Swagger en `/docs`
- Los logs se muestran en las ventanas de cada servicio
- Usa `Ctrl+C` en cada ventana para detener un servicio específico

## 🎯 Próximos Pasos

1. ✅ Iniciar servicios
2. ✅ Configurar datos de prueba
3. ✅ Probar endpoints en http://localhost:8000/docs
4. 🚀 Desarrollar frontend (opcional)
5. 🐳 Dockerizar servicios (opcional)
