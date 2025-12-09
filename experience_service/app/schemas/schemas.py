from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ExperienceBase(BaseModel):
    title: str
    content: str
    rating: int = Field(ge=1, le=5)
    category: str
    is_public: bool = True


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    category: Optional[str] = None
    is_public: Optional[bool] = None


class ExperienceResponse(ExperienceBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
