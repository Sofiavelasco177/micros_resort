from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.connection import get_db
from ..schemas.schemas import (
    RoomCreate, RoomUpdate, RoomResponse, RoomWithInventory,
    InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse,
    MessageResponse
)
from ..services.room_service import RoomService
from ..api.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=List[RoomResponse])
def get_rooms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar todas las habitaciones"""
    service = RoomService(db)
    return service.get_all_rooms(skip, limit)


@router.get("/available", response_model=List[RoomResponse])
def get_available_rooms(
    room_type: Optional[str] = Query(None, description="Filtrar por tipo: single, double, suite, deluxe"),
    db: Session = Depends(get_db)
):
    """Obtener habitaciones disponibles"""
    service = RoomService(db)
    return service.get_available_rooms(room_type)


@router.get("/{room_id}", response_model=RoomWithInventory)
def get_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    """Obtener habitación por ID con su inventario"""
    service = RoomService(db)
    return service.get_room_by_id(room_id)


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    room_data: RoomCreate,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Crear nueva habitación (solo admin)"""
    service = RoomService(db)
    return service.create_room(room_data)


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    room_data: RoomUpdate,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Actualizar habitación (solo admin)"""
    service = RoomService(db)
    return service.update_room(room_id, room_data)


@router.delete("/{room_id}", response_model=MessageResponse)
def delete_room(
    room_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Eliminar habitación (solo admin)"""
    service = RoomService(db)
    service.delete_room(room_id)
    return MessageResponse(message="Habitación eliminada exitosamente")


# Endpoints de inventario
@router.get("/{room_id}/inventory", response_model=List[InventoryItemResponse])
def get_room_inventory(
    room_id: int,
    db: Session = Depends(get_db)
):
    """Ver inventario de una habitación"""
    service = RoomService(db)
    return service.get_room_inventory(room_id)


@router.post("/{room_id}/inventory", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED)
def add_inventory_item(
    room_id: int,
    item_data: InventoryItemCreate,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Agregar item al inventario (solo admin)"""
    service = RoomService(db)
    return service.add_inventory_item(room_id, item_data)


@router.put("/{room_id}/inventory/{item_id}", response_model=InventoryItemResponse)
def update_inventory_item(
    room_id: int,
    item_id: int,
    item_data: InventoryItemUpdate,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Actualizar item del inventario (solo admin)"""
    service = RoomService(db)
    return service.update_inventory_item(room_id, item_id, item_data)


@router.delete("/{room_id}/inventory/{item_id}", response_model=MessageResponse)
def delete_inventory_item(
    room_id: int,
    item_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Eliminar item del inventario (solo admin)"""
    service = RoomService(db)
    service.delete_inventory_item(room_id, item_id)
    return MessageResponse(message="Item eliminado exitosamente")
