from pydantic import BaseModel

class NossocontatoBase(BaseModel):
    tipo: str
    local: str
    telefone: str
    email: str

class NossocontatoCreate(NossocontatoBase):
    pass

class Nossocontato(NossocontatoBase):
    id: int | None = None
    
    class Config:
        orm_mode = True