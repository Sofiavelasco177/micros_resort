from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime
from ..models.models import Room, RoomInventory
from ..schemas.schemas import RoomCreate, RoomUpdate, InventoryItemCreate, InventoryItemUpdate


class RoomService:
    """Servicio de gestión de habitaciones"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_rooms(self, skip: int = 0, limit: int = 100) -> List[Room]:
        """Obtener todas las habitaciones"""
        return self.db.query(Room).offset(skip).limit(limit).all()
    
    def get_room_by_id(self, room_id: int) -> Room:
        """Obtener habitación por ID"""
        room = self.db.query(Room).filter(Room.id == room_id).first()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Habitación no encontrada"
            )
        return room
    
    def get_room_by_number(self, room_number: str) -> Optional[Room]:
        """Obtener habitación por número"""
        return self.db.query(Room).filter(Room.room_number == room_number).first()
    
    def create_room(self, room_data: RoomCreate) -> Room:
        """Crear nueva habitación"""
        # Verificar si el número de habitación ya existe
        existing_room = self.get_room_by_number(room_data.room_number)
        if existing_room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de habitación ya existe"
            )
        
        db_room = Room(**room_data.model_dump())
        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return db_room
    
    def update_room(self, room_id: int, room_data: RoomUpdate) -> Room:
        """Actualizar habitación"""
        db_room = self.get_room_by_id(room_id)
        
        update_data = room_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_room, field, value)
        
        self.db.commit()
        self.db.refresh(db_room)
        return db_room
    
    def delete_room(self, room_id: int) -> bool:
        """Eliminar habitación"""
        db_room = self.get_room_by_id(room_id)
        self.db.delete(db_room)
        self.db.commit()
        return True
    
    def get_available_rooms(self, room_type: Optional[str] = None) -> List[Room]:
        """Obtener habitaciones disponibles"""
        query = self.db.query(Room).filter(Room.is_available == True)
        
        if room_type:
            query = query.filter(Room.type == room_type)
        
        return query.all()
    
    # Gestión de inventario
    def get_room_inventory(self, room_id: int) -> List[RoomInventory]:
        """Obtener inventario de una habitación"""
        self.get_room_by_id(room_id)  # Verificar que la habitación existe
        return self.db.query(RoomInventory).filter(RoomInventory.room_id == room_id).all()
    
    def add_inventory_item(self, room_id: int, item_data: InventoryItemCreate) -> RoomInventory:
        """Agregar item al inventario"""
        self.get_room_by_id(room_id)  # Verificar que la habitación existe
        
        db_item = RoomInventory(
            room_id=room_id,
            **item_data.model_dump()
        )
        
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def update_inventory_item(self, room_id: int, item_id: int, item_data: InventoryItemUpdate) -> RoomInventory:
        """Actualizar item del inventario"""
        db_item = self.db.query(RoomInventory).filter(
            RoomInventory.id == item_id,
            RoomInventory.room_id == room_id
        ).first()
        
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item de inventario no encontrado"
            )
        
        update_data = item_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db_item.last_checked = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def delete_inventory_item(self, room_id: int, item_id: int) -> bool:
        """Eliminar item del inventario"""
        db_item = self.db.query(RoomInventory).filter(
            RoomInventory.id == item_id,
            RoomInventory.room_id == room_id
        ).first()
        
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item de inventario no encontrado"
            )
        
        self.db.delete(db_item)
        self.db.commit()
        return True
