from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from ..database.connection import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False, index=True)  # appetizer, main, dessert, beverage
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)
    allergens = Column(JSON, nullable=True)  # ["gluten", "nuts", "dairy", etc.]


class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer, unique=True, nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    location = Column(String, nullable=False)  # indoor, outdoor, terrace, etc.
    is_available = Column(Boolean, default=True)
