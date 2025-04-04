from app.models.base import Base
from app.models.social_media import SocialMedia
from app.services.database import engine

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Add initial social media data
    from app.services.database import SessionLocal
    db = SessionLocal()
    
    try:
        if not db.query(SocialMedia).first():
            social_media = [
                SocialMedia(name="Facebook", url="https://facebook.com/mibitech", icon="fab fa-facebook-f"),
                SocialMedia(name="Instagram", url="https://instagram.com/mibitech", icon="fab fa-instagram"),
                SocialMedia(name="LinkedIn", url="https://linkedin.com/company/mibitech", icon="fab fa-linkedin-in"),
                SocialMedia(name="GitHub", url="https://github.com/mibitech", icon="fab fa-github")
            ]
            db.add_all(social_media)
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()