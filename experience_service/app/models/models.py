from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..database.connection import Base


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(String(2000), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    category = Column(String(50), nullable=False, index=True)  # accommodation, restaurant, spa, activities, general
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
