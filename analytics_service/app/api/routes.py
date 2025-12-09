from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from datetime import date, timedelta
from ..schemas.schemas import (
    DashboardResponse,
    RoomOccupancyResponse,
    RestaurantBookingsResponse,
    RevenueResponse,
    UserActivityResponse,
    ExperiencesSummaryResponse
)
from ..services.analytics_service import AnalyticsService
from .dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    current_user: dict = Depends(get_current_user)
):
    """Get overall dashboard statistics (admin only)"""
    data = AnalyticsService.get_dashboard_data()
    return DashboardResponse(**data)


@router.get("/rooms/occupancy", response_model=List[RoomOccupancyResponse])
def get_room_occupancy(
    start_date: date = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(default=None, description="End date (YYYY-MM-DD)"),
    current_user: dict = Depends(get_current_user)
):
    """Get room occupancy data for a date range (admin only)"""
    if not start_date:
        start_date = date.today() - timedelta(days=7)
    if not end_date:
        end_date = date.today()
    
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    data = AnalyticsService.get_room_occupancy(start_date, end_date)
    return [RoomOccupancyResponse(**item) for item in data]


@router.get("/restaurant/bookings", response_model=List[RestaurantBookingsResponse])
def get_restaurant_bookings(
    start_date: date = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(default=None, description="End date (YYYY-MM-DD)"),
    current_user: dict = Depends(get_current_user)
):
    """Get restaurant booking statistics for a date range (admin only)"""
    if not start_date:
        start_date = date.today() - timedelta(days=7)
    if not end_date:
        end_date = date.today()
    
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    data = AnalyticsService.get_restaurant_bookings(start_date, end_date)
    return [RestaurantBookingsResponse(**item) for item in data]


@router.get("/revenue", response_model=RevenueResponse)
def get_revenue(
    period: str = Query(default="daily", pattern="^(daily|weekly|monthly)$"),
    current_user: dict = Depends(get_current_user)
):
    """Get revenue data by period (admin only)"""
    data = AnalyticsService.get_revenue_data(period)
    return RevenueResponse(**data)


@router.get("/users/activity", response_model=List[UserActivityResponse])
def get_user_activity(
    start_date: date = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(default=None, description="End date (YYYY-MM-DD)"),
    current_user: dict = Depends(get_current_user)
):
    """Get user activity statistics for a date range (admin only)"""
    if not start_date:
        start_date = date.today() - timedelta(days=7)
    if not end_date:
        end_date = date.today()
    
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    data = AnalyticsService.get_user_activity(start_date, end_date)
    return [UserActivityResponse(**item) for item in data]


@router.get("/experiences/summary", response_model=ExperiencesSummaryResponse)
def get_experiences_summary(
    current_user: dict = Depends(get_current_user)
):
    """Get summary of user experiences and reviews (admin only)"""
    data = AnalyticsService.get_experiences_summary()
    return ExperiencesSummaryResponse(**data)
