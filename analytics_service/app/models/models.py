from sqlalchemy import Column, Integer, String, Float, DateTime, Date, JSON
from datetime import datetime
from ..database.connection import Base


class DailyRoomOccupancy(Base):
    """Modelo para almacenar datos diarios de ocupación de habitaciones"""
    __tablename__ = "daily_room_occupancy"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    total_rooms = Column(Integer, nullable=False)
    occupied_rooms = Column(Integer, nullable=False)
    occupancy_rate = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DailyRoomOccupancy(date={self.date}, occupancy_rate={self.occupancy_rate}%)>"


class DailyRestaurantBooking(Base):
    """Modelo para almacenar datos diarios de reservas de restaurantes"""
    __tablename__ = "daily_restaurant_bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    total_bookings = Column(Integer, nullable=False)
    completed_bookings = Column(Integer, nullable=False)
    cancelled_bookings = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DailyRestaurantBooking(date={self.date}, total={self.total_bookings})>"


class DailyRevenue(Base):
    """Modelo para almacenar datos diarios de ingresos"""
    __tablename__ = "daily_revenue"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    room_revenue = Column(Float, nullable=False, default=0.0)
    restaurant_revenue = Column(Float, nullable=False, default=0.0)
    experience_revenue = Column(Float, nullable=False, default=0.0)
    total_revenue = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DailyRevenue(date={self.date}, total={self.total_revenue})>"


class DailyUserActivity(Base):
    """Modelo para almacenar datos diarios de actividad de usuarios"""
    __tablename__ = "daily_user_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    active_users = Column(Integer, nullable=False)
    new_users = Column(Integer, nullable=False)
    total_bookings = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DailyUserActivity(date={self.date}, active_users={self.active_users})>"


class ExperienceMetrics(Base):
    """Modelo para almacenar métricas de experiencias"""
    __tablename__ = "experience_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    experience_id = Column(Integer, nullable=False, index=True)
    experience_name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    total_bookings = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    total_revenue = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ExperienceMetrics(name={self.experience_name}, rating={self.average_rating})>"


class SystemMetrics(Base):
    """Modelo para almacenar métricas generales del sistema"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_date = Column(DateTime, nullable=False, index=True)
    total_rooms = Column(Integer, default=0)
    total_reservations = Column(Integer, default=0)
    total_users = Column(Integer, default=0)
    total_restaurants = Column(Integer, default=0)
    total_experiences = Column(Integer, default=0)
    system_health = Column(String(20), default="healthy")  # healthy, degraded, down
    metadata = Column(JSON)  # Información adicional en formato JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SystemMetrics(date={self.metric_date}, health={self.system_health})>"
