from pydantic import BaseModel, EmailStr, constr

class MensagemBase(BaseModel):
    snome: constr(max_length=50)
    semail: EmailStr
    stelefone: constr(max_length=14)
    sassunto: constr(max_length=30)
    smensagem: constr(max_length=400)

class MensagemCreate(MensagemBase):
    pass

class Mensagem(MensagemBase):
    id: int
    
    class Config:
        orm_mode = True