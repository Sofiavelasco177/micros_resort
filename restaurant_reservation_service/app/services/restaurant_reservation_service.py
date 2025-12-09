from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.models import RestaurantReservation
from ..schemas.schemas import RestaurantReservationCreate, RestaurantReservationUpdate
from typing import List, Optional


class RestaurantReservationService:
    
    @staticmethod
    def get_all_reservations(db: Session, skip: int = 0, limit: int = 100) -> List[RestaurantReservation]:
        return db.query(RestaurantReservation).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_reservations_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[RestaurantReservation]:
        return db.query(RestaurantReservation).filter(
            RestaurantReservation.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_reservation_by_id(db: Session, reservation_id: int) -> Optional[RestaurantReservation]:
        return db.query(RestaurantReservation).filter(
            RestaurantReservation.id == reservation_id
        ).first()
    
    @staticmethod
    def create_reservation(
        db: Session, 
        reservation: RestaurantReservationCreate, 
        user_id: int
    ) -> RestaurantReservation:
        db_reservation = RestaurantReservation(
            user_id=user_id,
            table_id=reservation.table_id,
            reservation_date=reservation.reservation_date,
            reservation_time=reservation.reservation_time,
            guests_count=reservation.guests_count,
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
        reservation_update: RestaurantReservationUpdate,
        user_id: int
    ) -> Optional[RestaurantReservation]:
        db_reservation = db.query(RestaurantReservation).filter(
            RestaurantReservation.id == reservation_id,
            RestaurantReservation.user_id == user_id
        ).first()
        
        if not db_reservation:
            return None
        
        update_data = reservation_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reservation, field, value)
        
        db.commit()
        db.refresh(db_reservation)
        return db_reservation
    
    @staticmethod
    def delete_reservation(db: Session, reservation_id: int, user_id: int) -> bool:
        db_reservation = db.query(RestaurantReservation).filter(
            RestaurantReservation.id == reservation_id,
            RestaurantReservation.user_id == user_id
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
    ) -> Optional[RestaurantReservation]:
        db_reservation = db.query(RestaurantReservation).filter(
            RestaurantReservation.id == reservation_id,
            RestaurantReservation.user_id == user_id
        ).first()
        
        if not db_reservation:
            return None
        
        db_reservation.status = status
        db.commit()
        db.refresh(db_reservation)
        return db_reservation
