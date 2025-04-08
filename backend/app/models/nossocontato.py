from sqlalchemy import Column, Integer, String
from app.services.database import Base

class Nossocontato(Base):
    __tablename__ = 'nossocontato'
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)
    local = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)