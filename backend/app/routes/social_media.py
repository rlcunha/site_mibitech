from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.social_media import SocialMedia
from ..services.database import get_db
from ..schemas.social_media import SocialMediaSchema

router = APIRouter()

@router.get("/", response_model=list[SocialMediaSchema])
async def get_social_media(db: Session = Depends(get_db)):
    """Get all social media links"""
    return db.query(SocialMedia).all()