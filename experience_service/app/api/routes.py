from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..schemas.schemas import (
    ExperienceCreate,
    ExperienceUpdate,
    ExperienceResponse
)
from ..services.experience_service import ExperienceService
from .dependencies import get_current_user

router = APIRouter(prefix="/experiences", tags=["Experiences"])


@router.get("/", response_model=List[ExperienceResponse])
def get_all_experiences(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all experiences (admin only in production)"""
    experiences = ExperienceService.get_all_experiences(db, skip, limit)
    return experiences


@router.get("/public", response_model=List[ExperienceResponse])
def get_public_experiences(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all public experiences (no authentication required)"""
    experiences = ExperienceService.get_public_experiences(db, skip, limit)
    return experiences


@router.get("/{experience_id}", response_model=ExperienceResponse)
def get_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific experience by ID"""
    experience = ExperienceService.get_experience_by_id(db, experience_id)
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found"
        )
    
    # Only owner or public experiences can be viewed
    if not experience.is_public and experience.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this experience"
        )
    
    return experience


@router.post("/", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
def create_experience(
    experience: ExperienceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new experience"""
    return ExperienceService.create_experience(db, experience, current_user["user_id"])


@router.put("/{experience_id}", response_model=ExperienceResponse)
def update_experience(
    experience_id: int,
    experience_update: ExperienceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update an experience"""
    experience = ExperienceService.update_experience(
        db, experience_id, experience_update, current_user["user_id"]
    )
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found or not authorized"
        )
    return experience


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete an experience"""
    success = ExperienceService.delete_experience(db, experience_id, current_user["user_id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found or not authorized"
        )
    return None
