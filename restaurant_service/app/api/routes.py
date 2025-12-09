from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..schemas.schemas import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse,
    RestaurantTableCreate,
    RestaurantTableUpdate,
    RestaurantTableResponse
)
from ..services.restaurant_service import RestaurantService
from .dependencies import get_current_user

router = APIRouter(tags=["Restaurant"])

# Menu Item Endpoints
@router.get("/menu", response_model=List[MenuItemResponse])
def get_menu_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all menu items"""
    items = RestaurantService.get_all_menu_items(db, skip, limit)
    return items


@router.get("/menu/{item_id}", response_model=MenuItemResponse)
def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific menu item by ID"""
    item = RestaurantService.get_menu_item_by_id(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return item


@router.post("/menu", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu_item(
    item: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new menu item (admin only)"""
    return RestaurantService.create_menu_item(db, item)


@router.put("/menu/{item_id}", response_model=MenuItemResponse)
def update_menu_item(
    item_id: int,
    item_update: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update a menu item (admin only)"""
    item = RestaurantService.update_menu_item(db, item_id, item_update)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return item


@router.delete("/menu/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a menu item (admin only)"""
    success = RestaurantService.delete_menu_item(db, item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return None


# Restaurant Table Endpoints
@router.get("/tables", response_model=List[RestaurantTableResponse])
def get_tables(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all restaurant tables"""
    tables = RestaurantService.get_all_tables(db, skip, limit)
    return tables


@router.get("/tables/{table_id}", response_model=RestaurantTableResponse)
def get_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific table by ID"""
    table = RestaurantService.get_table_by_id(db, table_id)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    return table


@router.post("/tables", response_model=RestaurantTableResponse, status_code=status.HTTP_201_CREATED)
def create_table(
    table: RestaurantTableCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new restaurant table (admin only)"""
    return RestaurantService.create_table(db, table)


@router.put("/tables/{table_id}", response_model=RestaurantTableResponse)
def update_table(
    table_id: int,
    table_update: RestaurantTableUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update a restaurant table (admin only)"""
    table = RestaurantService.update_table(db, table_id, table_update)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    return table


@router.delete("/tables/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a restaurant table (admin only)"""
    success = RestaurantService.delete_table(db, table_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    return None
