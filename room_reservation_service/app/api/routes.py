from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..schemas.schemas import (
    RoomReservationCreate,
    RoomReservationUpdate,
    RoomReservationResponse,
    RoomReservationStatusUpdate,
    CheckAvailabilityRequest,
    CheckAvailabilityResponse
)
from ..services.room_reservation_service import RoomReservationService
from .dependencies import get_current_user

router = APIRouter(prefix="/reservations/rooms", tags=["Room Reservations"])


@router.get("/", response_model=List[RoomReservationResponse])
def get_all_reservations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all room reservations (admin only in production)"""
    reservations = RoomReservationService.get_all_reservations(db, skip, limit)
    return reservations


@router.get("/my", response_model=List[RoomReservationResponse])
def get_my_reservations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get current user's room reservations"""
    reservations = RoomReservationService.get_reservations_by_user(
        db, current_user["user_id"], skip, limit
    )
    return reservations


@router.get("/{reservation_id}", response_model=RoomReservationResponse)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific room reservation by ID"""
    reservation = RoomReservationService.get_reservation_by_id(db, reservation_id)
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


@router.post("/", response_model=RoomReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation: RoomReservationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new room reservation"""
    # Validate dates
    if reservation.check_out_date <= reservation.check_in_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out date must be after check-in date"
        )
    
    # Check availability
    is_available = RoomReservationService.check_availability(
        db, reservation.room_id, reservation.check_in_date, reservation.check_out_date
    )
    if not is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room is not available for the selected dates"
        )
    
    return RoomReservationService.create_reservation(db, reservation, current_user["user_id"])


@router.put("/{reservation_id}", response_model=RoomReservationResponse)
def update_reservation(
    reservation_id: int,
    reservation_update: RoomReservationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update a room reservation"""
    reservation = RoomReservationService.update_reservation(
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
    """Delete a room reservation"""
    success = RoomReservationService.delete_reservation(db, reservation_id, current_user["user_id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found or not authorized"
        )
    return None


@router.patch("/{reservation_id}/status", response_model=RoomReservationResponse)
def update_reservation_status(
    reservation_id: int,
    status_update: RoomReservationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update reservation status"""
    reservation = RoomReservationService.update_reservation_status(
        db, reservation_id, status_update.status, current_user["user_id"]
    )
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found or not authorized"
        )
    return reservation


@router.get("/check-availability", response_model=CheckAvailabilityResponse)
def check_availability(
    room_id: int,
    check_in_date: str,
    check_out_date: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Check if a room is available for specific dates"""
    from datetime import datetime
    
    try:
        check_in = datetime.strptime(check_in_date, "%Y-%m-%d").date()
        check_out = datetime.strptime(check_out_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    if check_out <= check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out date must be after check-in date"
        )
    
    is_available = RoomReservationService.check_availability(db, room_id, check_in, check_out)
    
    return CheckAvailabilityResponse(
        available=is_available,
        room_id=room_id,
        check_in_date=check_in,
        check_out_date=check_out
    )
