from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.nossocontato import Nossocontato as NossocontatoModel
from app.schemas.nossocontato import Nossocontato, NossocontatoCreate
from app.services.database import get_db

router = APIRouter(
    prefix="/api/v1/nossocontato",
    tags=["nossocontato"]
)

@router.get("/", response_model=List[Nossocontato])
def listar_contatos(db: Session = Depends(get_db)):
    return db.query(NossocontatoModel).all()

@router.post("/", status_code=201, response_model=NossocontatoCreate)
def criar_contato(
    contato: NossocontatoCreate,
    db: Session = Depends(get_db)
):
    db_contato = NossocontatoModel(
        tipo=contato.tipo,
        local=contato.local,
        telefone=contato.telefone,
        email=contato.email
    )
    db.add(db_contato)
    db.commit()
    db.refresh(db_contato)
    return db_contato