from typing import Optional
from pydantic import BaseModel

class NossocontatoBase(BaseModel):
    tipo: str
    local: str
    telefone: str
    email: str

class NossocontatoCreate(NossocontatoBase):
    pass

class Nossocontato(NossocontatoBase):
    id: Optional[int] = None
    
    class Config:
        from_attributes = True