from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.sql import func
from ..database.connection import Base


class RoomReservation(Base):
    __tablename__ = "room_reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    room_id = Column(Integer, nullable=False, index=True)
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    guests_count = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default="pending")  # pending, confirmed, cancelled, completed
    special_requests = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
