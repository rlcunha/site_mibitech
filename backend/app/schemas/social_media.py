from pydantic import BaseModel

class SocialMediaBase(BaseModel):
    name: str
    url: str
    icon: str

class SocialMediaCreate(SocialMediaBase):
    pass

class SocialMediaSchema(SocialMediaBase):
    id: int

    class Config:
        from_attributes = True