"""
Rotas para processamento de webhooks.

Este módulo implementa endpoints para receber e processar webhooks
de sistemas externos, com validação de segurança e processamento
de diferentes tipos de eventos.
"""
from fastapi import APIRouter, Depends, HTTPException, Header, Request, BackgroundTasks
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
import hashlib
import hmac
import uuid
import os
import json

from ..models.social_media import SocialMedia
from ..schemas.webhook import WebhookPayload, WebhookResponse, WebhookBatchResponse, WebhookEventType
from ..services.database import get_db
from ..errors import BaseAPIError, ValidationError
from ..helpers import DataProcessor, JsonProcessor, StringProcessor
from sqlalchemy.orm import Session

# Configuração de logging
logger = logging.getLogger("api.webhooks")

router = APIRouter()

# Segurança de webhook
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "default-secret")
VERIFY_SIGNATURES = os.getenv("VERIFY_SIGNATURES", "true").lower() == "true"

def verify_webhook(signature: str, payload: bytes) -> bool:
    """
    Verifica a assinatura do webhook para autenticidade.
    
    Usa HMAC com SHA-256 para verificar se o webhook foi enviado
    por uma fonte autorizada.
    
    Args:
        signature: Assinatura fornecida no cabeçalho
        payload: Corpo da requisição em bytes
        
    Returns:
        bool: True se a assinatura for válida, False caso contrário
    """
    # Se a verificação estiver desativada, sempre retorna True
    if not VERIFY_SIGNATURES:
        logger.warning("Verificação de assinatura de webhook desativada")
        return True
        
    # Se não houver assinatura, rejeita
    if not signature:
        logger.warning("Requisição de webhook sem assinatura")
        return False
        
    # Calcula o digest esperado
    digest = hmac.new(
        WEBHOOK_SECRET.encode(),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    # Compara de forma segura contra timing attacks
    is_valid = hmac.compare_digest(digest, signature)
    
    if not is_valid:
        logger.warning(f"Assinatura de webhook inválida: {signature}")
        
    return is_valid

class WebhookProcessor(DataProcessor):
    """
    Processador especializado para dados de webhook.
    
    Implementa lógica para transformar, validar e processar
    payloads de webhook recebidos.
    """
    
    def __init__(self):
        """Inicializa o processador com utilitários necessários."""
        self.json_processor = JsonProcessor()
        self.string_processor = StringProcessor()
    
    def process(self, data: dict) -> dict:
        """
        Transforma o payload do webhook.
        
        Args:
            data: Dados do webhook a serem processados
            
        Returns:
            Dados transformados
        """
        return {
            "event": data.get("event_type"),
            "payload": data.get("data"),
            "processed_at": datetime.now().isoformat(),
            "event_id": str(uuid.uuid4())
        }
    
    def validate(self, data: Any) -> bool:
        """
        Valida os dados do webhook.
        
        Args:
            data: Dados a serem validados
            
        Returns:
            bool: True se os dados são válidos, False caso contrário
        """
        if not isinstance(data, dict):
            return False
            
        required_fields = ["event_type", "data"]
        return all(field in data for field in required_fields)
    
    async def process_event(self, event_type: str, data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Processa um evento de webhook com base no tipo.
        
        Implementa lógica específica para cada tipo de evento suportado.
        
        Args:
            event_type: Tipo do evento a ser processado
            data: Dados associados ao evento
            db: Sessão do banco de dados
            
        Returns:
            Resultado do processamento
            
        Raises:
            ValidationError: Se os dados forem inválidos para o tipo de evento
        """
        # Registra o evento recebido
        logger.info(f"Processando evento de webhook: {event_type}")
        
        # Processa com base no tipo de evento
        if event_type == WebhookEventType.SOCIAL_MEDIA_UPDATE:
            # Valida dados específicos para atualização de mídia social
            required_fields = ["name", "url", "icon"]
            if not all(field in data for field in required_fields):
                raise ValidationError(
                    message="Dados incompletos para atualização de mídia social",
                    details={"required_fields": required_fields, "received": list(data.keys())}
                )
                
            # Cria ou atualiza registro de mídia social
            social_media = db.query(SocialMedia).filter_by(name=data["name"]).first()
            if social_media:
                # Atualiza registro existente
                for key, value in data.items():
                    setattr(social_media, key, value)
            else:
                # Cria novo registro
                social_media = SocialMedia(**data)
                db.add(social_media)
                
            db.commit()
            return {"id": social_media.id, "name": social_media.name, "action": "updated" if social_media else "created"}
            
        elif event_type == WebhookEventType.CONTACT_FORM:
            # Exemplo: processar submissão de formulário de contato
            logger.info(f"Formulário de contato recebido: {data.get('email')}")
            # Aqui implementaríamos lógica para salvar contato ou enviar email
            return {"contact_email": data.get("email"), "action": "processed"}
            
        elif event_type == WebhookEventType.PORTFOLIO_UPDATE:
            # Exemplo: processar atualização de portfólio
            logger.info(f"Atualização de portfólio recebida: {data.get('title')}")
            # Aqui implementaríamos lógica para atualizar portfólio
            return {"portfolio_item": data.get("title"), "action": "updated"}
            
        else:
            # Tipo de evento desconhecido ou personalizado
            logger.warning(f"Tipo de evento não implementado: {event_type}")
            return {"event_type": event_type, "action": "logged"}

def process_webhook_async(payload: Dict[str, Any], db: Session):
    """
    Processa webhook de forma assíncrona em background.
    
    Args:
        payload: Dados do webhook
        db: Sessão do banco de dados
    """
    processor = WebhookProcessor()
    try:
        event_type = payload.get("event_type")
        data = payload.get("data", {})
        
        # Aqui processaríamos o evento de forma assíncrona
        logger.info(f"Processando webhook assíncrono: {event_type}")
        
        # Exemplo: salvar no banco de dados
        if event_type == WebhookEventType.SOCIAL_MEDIA_UPDATE.value:
            social_media = SocialMedia(**data)
            db.add(social_media)
            db.commit()
            
    except Exception as e:
        logger.error(f"Erro no processamento assíncrono: {str(e)}")
        db.rollback()

@router.post("/", response_model=WebhookResponse)
async def handle_webhook(
    request: Request,
    payload: WebhookPayload,
    background_tasks: BackgroundTasks,
    x_hub_signature: Optional[str] = Header(None),
    process_async: bool = False,
    db: Session = Depends(get_db)
):
    """
    Manipula webhooks recebidos.
    
    Este endpoint recebe notificações de sistemas externos,
    verifica sua autenticidade e processa os dados conforme
    o tipo de evento.
    
    Args:
        request: Objeto de requisição FastAPI
        payload: Dados do webhook
        background_tasks: Gerenciador de tarefas em background
        x_hub_signature: Assinatura para verificação
        process_async: Se deve processar de forma assíncrona
        db: Sessão do banco de dados
        
    Returns:
        Resposta indicando o resultado do processamento
        
    Raises:
        BaseAPIError: Se ocorrer algum erro no processamento
    """
    try:
        # Registra recebimento do webhook
        logger.info(f"Webhook recebido: {payload.event_type}")
        
        # Verifica assinatura
        body = await request.body()
        if not verify_webhook(x_hub_signature, body):
            raise BaseAPIError(
                message="Assinatura de webhook inválida",
                status_code=401
            )

        # Processa dados
        processor = WebhookProcessor()
        processed = processor.process(payload.dict())
        
        # Gera ID do evento
        event_id = processed.get("event_id", hashlib.sha256(body).hexdigest())

        # Decide entre processamento síncrono ou assíncrono
        if process_async:
            # Agenda processamento em background
            background_tasks.add_task(
                process_webhook_async,
                payload.dict(),
                db
            )
            return WebhookResponse(
                status="pending",
                message="Webhook agendado para processamento",
                event_id=event_id,
                processed_at=datetime.now()
            )
        else:
            # Processamento síncrono
            result = await processor.process_event(
                payload.event_type,
                payload.data,
                db
            )
            
            return WebhookResponse(
                status="success",
                message="Webhook processado com sucesso",
                event_id=event_id,
                processed_at=datetime.now()
            )

    except ValidationError as e:
        # Erro de validação específico
        raise e
    except Exception as e:
        # Registra erro detalhado
        logger.error(f"Falha no processamento de webhook: {str(e)}", exc_info=True)
        
        raise BaseAPIError(
            message="Falha no processamento do webhook",
            status_code=500,
            details={"error": str(e)}
        )

@router.post("/batch", response_model=WebhookBatchResponse)
async def handle_webhook_batch(
    request: Request,
    payloads: List[WebhookPayload],
    x_hub_signature: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Processa múltiplos webhooks em uma única requisição.
    
    Útil para sistemas que precisam enviar vários eventos de uma vez.
    
    Args:
        request: Objeto de requisição FastAPI
        payloads: Lista de payloads de webhook
        x_hub_signature: Assinatura para verificação
        db: Sessão do banco de dados
        
    Returns:
        Resumo do processamento em lote
    """
    try:
        # Verifica assinatura
        body = await request.body()
        if not verify_webhook(x_hub_signature, body):
            raise BaseAPIError(
                message="Assinatura de webhook inválida",
                status_code=401
            )
            
        # Processa cada webhook
        processor = WebhookProcessor()
        results = []
        successful = 0
        failed = 0
        
        for payload in payloads:
            try:
                processed = processor.process(payload.dict())
                await processor.process_event(
                    payload.event_type,
                    payload.data,
                    db
                )
                
                results.append(WebhookResponse(
                    status="success",
                    message="Processado com sucesso",
                    event_id=processed.get("event_id", str(uuid.uuid4())),
                    processed_at=datetime.now()
                ))
                successful += 1
                
            except Exception as e:
                results.append(WebhookResponse(
                    status="error",
                    message=f"Falha: {str(e)}",
                    event_id=str(uuid.uuid4()),
                    processed_at=datetime.now()
                ))
                failed += 1
                
        return WebhookBatchResponse(
            total_processed=len(payloads),
            successful=successful,
            failed=failed,
            results=results
        )
            
    except Exception as e:
        raise BaseAPIError(
            message="Falha no processamento em lote",
            status_code=500,
            details={"error": str(e)}
        )

@router.get("/data", response_model=List[Dict[str, Any]])
async def get_webhook_data(db: Session = Depends(get_db)):
    """
    Obtém dados para consumidores de webhook.
    
    Retorna dados que podem ser consumidos por sistemas externos
    via webhook.
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Lista de dados formatados para webhook
    """
    try:
        processor = WebhookProcessor()
        data = db.query(SocialMedia).all()
        
        # Converte objetos do modelo para dicionários e processa
        results = []
        for item in data:
            # Converte para dict excluindo atributos SQLAlchemy
            item_dict = {c.name: getattr(item, c.name) for c in item.__table__.columns}
            results.append(processor.process({
                "event_type": "social_media_data",
                "data": item_dict
            }))
            
        return results
        
    except Exception as e:
        logger.error(f"Erro ao buscar dados de webhook: {str(e)}", exc_info=True)
        raise BaseAPIError(
            message="Falha ao buscar dados de webhook",
            status_code=500,
            details={"error": str(e)}
        )