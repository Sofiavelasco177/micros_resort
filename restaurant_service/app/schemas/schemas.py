from pydantic import BaseModel, Field
from typing import Optional, List


# MenuItem Schemas
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: float = Field(gt=0)
    is_available: bool = True
    image_url: Optional[str] = None
    allergens: Optional[List[str]] = None


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None
    image_url: Optional[str] = None
    allergens: Optional[List[str]] = None


class MenuItemResponse(MenuItemBase):
    id: int

    class Config:
        from_attributes = True


# RestaurantTable Schemas
class RestaurantTableBase(BaseModel):
    table_number: int
    capacity: int = Field(gt=0)
    location: str
    is_available: bool = True


class RestaurantTableCreate(RestaurantTableBase):
    pass


class RestaurantTableUpdate(BaseModel):
    table_number: Optional[int] = None
    capacity: Optional[int] = Field(None, gt=0)
    location: Optional[str] = None
    is_available: Optional[bool] = None


class RestaurantTableResponse(RestaurantTableBase):
    id: int

    class Config:
        from_attributes = True
