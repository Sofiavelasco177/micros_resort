from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..schemas.schemas import (
    RestaurantReservationCreate,
    RestaurantReservationUpdate,
    RestaurantReservationResponse,
    RestaurantReservationStatusUpdate
)
from ..services.restaurant_reservation_service import RestaurantReservationService
from .dependencies import get_current_user

router = APIRouter(prefix="/reservations/restaurant", tags=["Restaurant Reservations"])


@router.get("/", response_model=List[RestaurantReservationResponse])
def get_all_reservations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all restaurant reservations (admin only in production)"""
    reservations = RestaurantReservationService.get_all_reservations(db, skip, limit)
    return reservations


@router.get("/my", response_model=List[RestaurantReservationResponse])
def get_my_reservations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get current user's restaurant reservations"""
    reservations = RestaurantReservationService.get_reservations_by_user(
        db, current_user["user_id"], skip, limit
    )
    return reservations


@router.get("/{reservation_id}", response_model=RestaurantReservationResponse)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific restaurant reservation by ID"""
    reservation = RestaurantReservationService.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    if reservation.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this reservation"
        )
    return reservation


@router.post("/", response_model=RestaurantReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation: RestaurantReservationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new restaurant reservation"""
    return RestaurantReservationService.create_reservation(
        db, reservation, current_user["user_id"]
    )


@router.put("/{reservation_id}", response_model=RestaurantReservationResponse)
def update_reservation(
    reservation_id: int,
    reservation_update: RestaurantReservationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update a restaurant reservation"""
    reservation = RestaurantReservationService.update_reservation(
        db, reservation_id, reservation_update, current_user["user_id"]
    )
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found or not authorized"
        )
    return reservation


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a restaurant reservation"""
    success = RestaurantReservationService.delete_reservation(
        db, reservation_id, current_user["user_id"]
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found or not authorized"
        )
    return None


@router.patch("/{reservation_id}/status", response_model=RestaurantReservationResponse)
def update_reservation_status(
    reservation_id: int,
    status_update: RestaurantReservationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update restaurant reservation status"""
    reservation = RestaurantReservationService.update_reservation_status(
        db, reservation_id, status_update.status, current_user["user_id"]
    )
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found or not authorized"
        )
    return reservation
