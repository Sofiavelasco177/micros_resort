from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import Optional


class RestaurantReservationBase(BaseModel):
    table_id: int
    reservation_date: date
    reservation_time: time
    guests_count: int = Field(gt=0)
    special_requests: Optional[str] = None


class RestaurantReservationCreate(RestaurantReservationBase):
    pass


class RestaurantReservationUpdate(BaseModel):
    table_id: Optional[int] = None
    reservation_date: Optional[date] = None
    reservation_time: Optional[time] = None
    guests_count: Optional[int] = Field(None, gt=0)
    special_requests: Optional[str] = None


class RestaurantReservationStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|confirmed|cancelled|completed)$")


class RestaurantReservationResponse(RestaurantReservationBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
