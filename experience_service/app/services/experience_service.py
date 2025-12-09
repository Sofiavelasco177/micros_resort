from sqlalchemy.orm import Session
from ..models.models import Experience
from ..schemas.schemas import ExperienceCreate, ExperienceUpdate
from typing import List, Optional


class ExperienceService:
    
    @staticmethod
    def get_all_experiences(db: Session, skip: int = 0, limit: int = 100) -> List[Experience]:
        return db.query(Experience).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_public_experiences(db: Session, skip: int = 0, limit: int = 100) -> List[Experience]:
        return db.query(Experience).filter(
            Experience.is_public == True
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_experience_by_id(db: Session, experience_id: int) -> Optional[Experience]:
        return db.query(Experience).filter(Experience.id == experience_id).first()
    
    @staticmethod
    def create_experience(db: Session, experience: ExperienceCreate, user_id: int) -> Experience:
        db_experience = Experience(
            user_id=user_id,
            **experience.model_dump()
        )
        db.add(db_experience)
        db.commit()
        db.refresh(db_experience)
        return db_experience
    
    @staticmethod
    def update_experience(
        db: Session, 
        experience_id: int, 
        experience_update: ExperienceUpdate,
        user_id: int
    ) -> Optional[Experience]:
        db_experience = db.query(Experience).filter(
            Experience.id == experience_id,
            Experience.user_id == user_id
        ).first()
        
        if not db_experience:
            return None
        
        update_data = experience_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_experience, field, value)
        
        db.commit()
        db.refresh(db_experience)
        return db_experience
    
    @staticmethod
    def delete_experience(db: Session, experience_id: int, user_id: int) -> bool:
        db_experience = db.query(Experience).filter(
            Experience.id == experience_id,
            Experience.user_id == user_id
        ).first()
        
        if not db_experience:
            return False
        
        db.delete(db_experience)
        db.commit()
        return True
