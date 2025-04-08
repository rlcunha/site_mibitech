from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.models.mensagem import Mensagem
from app.schemas.mensagem import MensagemCreate
from app.services.database import get_db

logger = logging.getLogger("api.mensagem")
if not logger.handlers:  # Evita adicionar múltiplos handlers
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

router = APIRouter(
    prefix="/api/v1/mensagem",
    tags=["mensagens"]
)

@router.post("/", status_code=201, response_model=MensagemCreate)
async def criar_mensagem(
    mensagem: MensagemCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para criação de novas mensagens de clientes
    
    Args:
        mensagem: Dados da mensagem validados
        db: Sessão do banco de dados
        
    Returns:
        Mensagem criada com ID
    """
    try:
        logger.info(f"Recebendo mensagem - Nome: {mensagem.snome}, Email: {mensagem.semail[:3]}..., Assunto: {mensagem.sassunto}")
        
        nova_mensagem = Mensagem(
            snome=mensagem.snome,
            semail=mensagem.semail,
            stelefone=mensagem.stelefone,
            sassunto=mensagem.sassunto,
            smensagem=mensagem.smensagem
        )

        logger.debug(f"Objeto mensagem criado")
        
        db.add(nova_mensagem)
        db.commit()
        db.refresh(nova_mensagem)

        logger.info(f"Mensagem registrada - ID: {nova_mensagem.id}")
        
        return nova_mensagem
        
    except Exception as e:
        logger.error(f"Erro ao criar mensagem: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Falha ao registrar mensagem"
        )