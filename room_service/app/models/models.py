from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base


class Room(Base):
    """Modelo de habitación"""
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(10), unique=True, nullable=False, index=True)
    type = Column(String(50), nullable=False)  # single, double, suite, deluxe
    price_per_night = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False)
    description = Column(Text)
    amenities = Column(JSON)  # ["wifi", "tv", "minibar", "balcony"]
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con inventario
    inventory_items = relationship("RoomInventory", back_populates="room", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Room(number={self.room_number}, type={self.type})>"


class RoomInventory(Base):
    """Modelo de inventario de habitación"""
    __tablename__ = "room_inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    item_name = Column(String(100), nullable=False)
    quantity = Column(Integer, default=1)
    condition = Column(String(20), default="good")  # good, fair, poor
    last_checked = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    # Relación con habitación
    room = relationship("Room", back_populates="inventory_items")
    
    def __repr__(self):
        return f"<RoomInventory(room_id={self.room_id}, item={self.item_name})>"
