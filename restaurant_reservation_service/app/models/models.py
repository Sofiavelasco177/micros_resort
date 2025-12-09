from sqlalchemy import Column, Integer, String, DateTime, Date, Time
from sqlalchemy.sql import func
from ..database.connection import Base


class RestaurantReservation(Base):
    __tablename__ = "restaurant_reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    table_id = Column(Integer, nullable=False, index=True)
    reservation_date = Column(Date, nullable=False)
    reservation_time = Column(Time, nullable=False)
    guests_count = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, confirmed, cancelled, completed
    special_requests = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
