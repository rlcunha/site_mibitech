from sqlalchemy import Column, Integer, String
from .base import Base

class Mensagem(Base):
    __tablename__ = 'mensagem'
    
    id = Column(Integer, primary_key=True, index=True)
    snome = Column(String(50))
    semail = Column(String(50))
    stelefone = Column(String(14))
    sassunto = Column(String(30))
    smensagem = Column(String(400))