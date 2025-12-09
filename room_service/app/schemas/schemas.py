from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class RoomBase(BaseModel):
    room_number: str
    type: str = Field(..., description="single, double, suite, deluxe")
    price_per_night: float = Field(..., gt=0)
    capacity: int = Field(..., gt=0)
    description: str
    amenities: List[str] = []


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    type: Optional[str] = None
    price_per_night: Optional[float] = None
    capacity: Optional[int] = None
    description: Optional[str] = None
    amenities: Optional[List[str]] = None
    is_available: Optional[bool] = None


class RoomResponse(RoomBase):
    id: int
    is_available: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class InventoryItemBase(BaseModel):
    item_name: str
    quantity: int = 1
    condition: str = Field(default="good", description="good, fair, poor")
    notes: Optional[str] = None


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemUpdate(BaseModel):
    item_name: Optional[str] = None
    quantity: Optional[int] = None
    condition: Optional[str] = None
    notes: Optional[str] = None


class InventoryItemResponse(InventoryItemBase):
    id: int
    room_id: int
    last_checked: datetime
    
    class Config:
        from_attributes = True


class RoomWithInventory(RoomResponse):
    inventory_items: List[InventoryItemResponse] = []


class MessageResponse(BaseModel):
    message: str
