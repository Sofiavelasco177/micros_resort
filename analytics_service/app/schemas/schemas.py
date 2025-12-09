from pydantic import BaseModel
from typing import Dict, List, Any
from datetime import date


class DashboardResponse(BaseModel):
    total_rooms: int
    occupied_rooms: int
    total_reservations: int
    total_revenue: float
    active_users: int
    restaurant_bookings: int


class RoomOccupancyResponse(BaseModel):
    date: date
    total_rooms: int
    occupied_rooms: int
    occupancy_rate: float
    revenue: float


class RestaurantBookingsResponse(BaseModel):
    date: date
    total_bookings: int
    completed_bookings: int
    cancelled_bookings: int


class RevenueResponse(BaseModel):
    period: str
    room_revenue: float
    restaurant_revenue: float
    total_revenue: float


class UserActivityResponse(BaseModel):
    date: date
    active_users: int
    new_users: int
    total_bookings: int


class ExperiencesSummaryResponse(BaseModel):
    total_experiences: int
    average_rating: float
    category_breakdown: Dict[str, int]
    recent_experiences: List[Dict[str, Any]]
