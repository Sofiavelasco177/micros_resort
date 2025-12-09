from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class RoomReservationBase(BaseModel):
    room_id: int
    check_in_date: date
    check_out_date: date
    guests_count: int = Field(gt=0)
    special_requests: Optional[str] = None


class RoomReservationCreate(RoomReservationBase):
    pass


class RoomReservationUpdate(BaseModel):
    room_id: Optional[int] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    guests_count: Optional[int] = Field(None, gt=0)
    special_requests: Optional[str] = None


class RoomReservationStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|confirmed|cancelled|completed)$")


class RoomReservationResponse(RoomReservationBase):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CheckAvailabilityRequest(BaseModel):
    room_id: int
    check_in_date: date
    check_out_date: date


class CheckAvailabilityResponse(BaseModel):
    available: bool
    room_id: int
    check_in_date: date
    check_out_date: date
