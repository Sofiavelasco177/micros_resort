from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from ..models.models import RoomReservation
from ..schemas.schemas import RoomReservationCreate, RoomReservationUpdate
from datetime import date
from typing import List, Optional


class RoomReservationService:
    
    @staticmethod
    def get_all_reservations(db: Session, skip: int = 0, limit: int = 100) -> List[RoomReservation]:
        return db.query(RoomReservation).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_reservations_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[RoomReservation]:
        return db.query(RoomReservation).filter(
            RoomReservation.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_reservation_by_id(db: Session, reservation_id: int) -> Optional[RoomReservation]:
        return db.query(RoomReservation).filter(RoomReservation.id == reservation_id).first()
    
    @staticmethod
    def create_reservation(db: Session, reservation: RoomReservationCreate, user_id: int) -> RoomReservation:
        # Calculate total price (simple calculation: days * base price)
        days = (reservation.check_out_date - reservation.check_in_date).days
        base_price_per_day = 100.0  # This should come from room service
        total_price = days * base_price_per_day
        
        db_reservation = RoomReservation(
            user_id=user_id,
            room_id=reservation.room_id,
            check_in_date=reservation.check_in_date,
            check_out_date=reservation.check_out_date,
            guests_count=reservation.guests_count,
            total_price=total_price,
            status="pending",
            special_requests=reservation.special_requests
        )
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        return db_reservation
    
    @staticmethod
    def update_reservation(
        db: Session, 
        reservation_id: int, 
        reservation_update: RoomReservationUpdate,
        user_id: int
    ) -> Optional[RoomReservation]:
        db_reservation = db.query(RoomReservation).filter(
            RoomReservation.id == reservation_id,
            RoomReservation.user_id == user_id
        ).first()
        
        if not db_reservation:
            return None
        
        update_data = reservation_update.model_dump(exclude_unset=True)
        
        # Recalculate total price if dates changed
        if "check_in_date" in update_data or "check_out_date" in update_data:
            check_in = update_data.get("check_in_date", db_reservation.check_in_date)
            check_out = update_data.get("check_out_date", db_reservation.check_out_date)
            days = (check_out - check_in).days
            base_price_per_day = 100.0
            update_data["total_price"] = days * base_price_per_day
        
        for field, value in update_data.items():
            setattr(db_reservation, field, value)
        
        db.commit()
        db.refresh(db_reservation)
        return db_reservation
    
    @staticmethod
    def delete_reservation(db: Session, reservation_id: int, user_id: int) -> bool:
        db_reservation = db.query(RoomReservation).filter(
            RoomReservation.id == reservation_id,
            RoomReservation.user_id == user_id
        ).first()
        
        if not db_reservation:
            return False
        
        db.delete(db_reservation)
        db.commit()
        return True
    
    @staticmethod
    def update_reservation_status(
        db: Session, 
        reservation_id: int, 
        status: str,
        user_id: int
    ) -> Optional[RoomReservation]:
        db_reservation = db.query(RoomReservation).filter(
            RoomReservation.id == reservation_id,
            RoomReservation.user_id == user_id
        ).first()
        
        if not db_reservation:
            return None
        
        db_reservation.status = status
        db.commit()
        db.refresh(db_reservation)
        return db_reservation
    
    @staticmethod
    def check_availability(
        db: Session, 
        room_id: int, 
        check_in_date: date, 
        check_out_date: date
    ) -> bool:
        # Check if there are any overlapping reservations
        overlapping = db.query(RoomReservation).filter(
            and_(
                RoomReservation.room_id == room_id,
                RoomReservation.status.in_(["pending", "confirmed"]),
                or_(
                    and_(
                        RoomReservation.check_in_date <= check_in_date,
                        RoomReservation.check_out_date > check_in_date
                    ),
                    and_(
                        RoomReservation.check_in_date < check_out_date,
                        RoomReservation.check_out_date >= check_out_date
                    ),
                    and_(
                        RoomReservation.check_in_date >= check_in_date,
                        RoomReservation.check_out_date <= check_out_date
                    )
                )
            )
        ).first()
        
        return overlapping is None
