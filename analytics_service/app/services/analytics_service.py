from datetime import date, timedelta, datetime
from typing import Dict, List, Any
import random


class AnalyticsService:
    """
    Analytics service that aggregates data from other microservices.
    In production, this would make HTTP requests to other services.
    For now, it returns mock data for demonstration.
    """
    
    @staticmethod
    def get_dashboard_data() -> Dict[str, Any]:
        """Get overall dashboard statistics"""
        return {
            "total_rooms": 50,
            "occupied_rooms": 35,
            "total_reservations": 127,
            "total_revenue": 45678.50,
            "active_users": 89,
            "restaurant_bookings": 234
        }
    
    @staticmethod
    def get_room_occupancy(start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get room occupancy data for a date range"""
        occupancy_data = []
        current_date = start_date
        
        while current_date <= end_date:
            total_rooms = 50
            occupied_rooms = random.randint(25, 48)
            occupancy_rate = (occupied_rooms / total_rooms) * 100
            revenue = occupied_rooms * 150.0  # Average room price
            
            occupancy_data.append({
                "date": current_date,
                "total_rooms": total_rooms,
                "occupied_rooms": occupied_rooms,
                "occupancy_rate": round(occupancy_rate, 2),
                "revenue": revenue
            })
            current_date += timedelta(days=1)
        
        return occupancy_data
    
    @staticmethod
    def get_restaurant_bookings(start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get restaurant booking statistics for a date range"""
        bookings_data = []
        current_date = start_date
        
        while current_date <= end_date:
            total_bookings = random.randint(20, 50)
            completed = random.randint(15, total_bookings - 2)
            cancelled = total_bookings - completed
            
            bookings_data.append({
                "date": current_date,
                "total_bookings": total_bookings,
                "completed_bookings": completed,
                "cancelled_bookings": cancelled
            })
            current_date += timedelta(days=1)
        
        return bookings_data
    
    @staticmethod
    def get_revenue_data(period: str) -> Dict[str, Any]:
        """Get revenue data by period (daily, weekly, monthly)"""
        if period == "daily":
            room_revenue = random.uniform(5000, 8000)
            restaurant_revenue = random.uniform(2000, 4000)
        elif period == "weekly":
            room_revenue = random.uniform(35000, 56000)
            restaurant_revenue = random.uniform(14000, 28000)
        else:  # monthly
            room_revenue = random.uniform(150000, 240000)
            restaurant_revenue = random.uniform(60000, 120000)
        
        return {
            "period": period,
            "room_revenue": round(room_revenue, 2),
            "restaurant_revenue": round(restaurant_revenue, 2),
            "total_revenue": round(room_revenue + restaurant_revenue, 2)
        }
    
    @staticmethod
    def get_user_activity(start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get user activity statistics for a date range"""
        activity_data = []
        current_date = start_date
        
        while current_date <= end_date:
            activity_data.append({
                "date": current_date,
                "active_users": random.randint(50, 150),
                "new_users": random.randint(5, 20),
                "total_bookings": random.randint(30, 70)
            })
            current_date += timedelta(days=1)
        
        return activity_data
    
    @staticmethod
    def get_experiences_summary() -> Dict[str, Any]:
        """Get summary of user experiences and reviews"""
        categories = ["accommodation", "restaurant", "spa", "activities", "general"]
        category_breakdown = {cat: random.randint(10, 50) for cat in categories}
        
        recent_experiences = [
            {
                "id": i,
                "title": f"Great Experience {i}",
                "rating": random.randint(3, 5),
                "category": random.choice(categories),
                "created_at": (datetime.now() - timedelta(days=i)).isoformat()
            }
            for i in range(1, 6)
        ]
        
        total_experiences = sum(category_breakdown.values())
        average_rating = round(random.uniform(4.0, 4.8), 2)
        
        return {
            "total_experiences": total_experiences,
            "average_rating": average_rating,
            "category_breakdown": category_breakdown,
            "recent_experiences": recent_experiences
        }
