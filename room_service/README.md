# Room Service

Servicio de gestión de habitaciones e inventario.

## Puerto: 8003

## Endpoints

### Habitaciones
- `GET /rooms/` - Listar habitaciones
- `GET /rooms/available` - Habitaciones disponibles
- `GET /rooms/{id}` - Obtener habitación con inventario
- `POST /rooms/` - Crear habitación (admin)
- `PUT /rooms/{id}` - Actualizar habitación (admin)
- `DELETE /rooms/{id}` - Eliminar habitación (admin)

### Inventario
- `GET /rooms/{id}/inventory` - Ver inventario
- `POST /rooms/{id}/inventory` - Agregar item (admin)
- `PUT /rooms/{id}/inventory/{item_id}` - Actualizar item (admin)
- `DELETE /rooms/{id}/inventory/{item_id}` - Eliminar item (admin)

## Ejecutar

```powershell
uvicorn app.main:app --reload --port 8003
```
