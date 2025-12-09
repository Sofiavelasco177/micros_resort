from sqlalchemy.orm import Session
from ..models.models import MenuItem, RestaurantTable
from ..schemas.schemas import MenuItemCreate, MenuItemUpdate, RestaurantTableCreate, RestaurantTableUpdate
from typing import List, Optional


class RestaurantService:
    
    # MenuItem methods
    @staticmethod
    def get_all_menu_items(db: Session, skip: int = 0, limit: int = 100) -> List[MenuItem]:
        return db.query(MenuItem).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_menu_item_by_id(db: Session, item_id: int) -> Optional[MenuItem]:
        return db.query(MenuItem).filter(MenuItem.id == item_id).first()
    
    @staticmethod
    def create_menu_item(db: Session, item: MenuItemCreate) -> MenuItem:
        db_item = MenuItem(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def update_menu_item(db: Session, item_id: int, item_update: MenuItemUpdate) -> Optional[MenuItem]:
        db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if not db_item:
            return None
        
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def delete_menu_item(db: Session, item_id: int) -> bool:
        db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if not db_item:
            return False
        
        db.delete(db_item)
        db.commit()
        return True
    
    # RestaurantTable methods
    @staticmethod
    def get_all_tables(db: Session, skip: int = 0, limit: int = 100) -> List[RestaurantTable]:
        return db.query(RestaurantTable).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_table_by_id(db: Session, table_id: int) -> Optional[RestaurantTable]:
        return db.query(RestaurantTable).filter(RestaurantTable.id == table_id).first()
    
    @staticmethod
    def create_table(db: Session, table: RestaurantTableCreate) -> RestaurantTable:
        db_table = RestaurantTable(**table.model_dump())
        db.add(db_table)
        db.commit()
        db.refresh(db_table)
        return db_table
    
    @staticmethod
    def update_table(db: Session, table_id: int, table_update: RestaurantTableUpdate) -> Optional[RestaurantTable]:
        db_table = db.query(RestaurantTable).filter(RestaurantTable.id == table_id).first()
        if not db_table:
            return None
        
        update_data = table_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_table, field, value)
        
        db.commit()
        db.refresh(db_table)
        return db_table
    
    @staticmethod
    def delete_table(db: Session, table_id: int) -> bool:
        db_table = db.query(RestaurantTable).filter(RestaurantTable.id == table_id).first()
        if not db_table:
            return False
        
        db.delete(db_table)
        db.commit()
        return True
