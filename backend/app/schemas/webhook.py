"""
Esquemas para processamento de webhooks.

Define os modelos de dados para receber e responder a webhooks.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class WebhookEventType(str, Enum):
    """
    Tipos de eventos suportados pelo sistema de webhook.
    
    Enum que define os tipos de eventos que podem ser processados.
    """
    SOCIAL_MEDIA_UPDATE = "social_media_update"
    CONTACT_FORM = "contact_form"
    PORTFOLIO_UPDATE = "portfolio_update"
    SYSTEM_NOTIFICATION = "system_notification"

class WebhookPayload(BaseModel):
    """
    Modelo para dados de entrada de webhook.
    
    Define a estrutura esperada para payloads de webhook recebidos.
    """
    event_type: str = Field(
        ...,
        description="Tipo do evento webhook"
    )
    data: Dict[str, Any] = Field(
        ...,
        description="Dados associados ao evento"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Momento em que o evento foi gerado"
    )
    signature: Optional[str] = Field(
        None,
        description="Assinatura para verificação de autenticidade"
    )
    
    @validator('event_type')
    def validate_event_type(cls, v):
        """
        Valida se o tipo de evento é suportado.
        
        Args:
            v: Valor do tipo de evento
            
        Returns:
            Valor validado
            
        Raises:
            ValueError: Se o tipo de evento não for suportado
        """
        try:
            return WebhookEventType(v)
        except ValueError:
            # Permite tipos personalizados, mas registra aviso
            valid_types = [e.value for e in WebhookEventType]
            if v not in valid_types:
                print(f"Aviso: Tipo de evento não padrão recebido: {v}")
            return v

class WebhookResponse(BaseModel):
    """
    Modelo para respostas de webhook.
    
    Define a estrutura das respostas enviadas após processamento de webhook.
    """
    status: str = Field(
        ...,
        description="Status do processamento (success/error)"
    )
    message: str = Field(
        ...,
        description="Mensagem descritiva do resultado"
    )
    event_id: str = Field(
        ...,
        description="Identificador único do evento processado"
    )
    processed_at: datetime = Field(
        default_factory=datetime.now,
        description="Momento em que o webhook foi processado"
    )
    
    @validator('status')
    def validate_status(cls, v):
        """
        Valida se o status é válido.
        
        Args:
            v: Valor do status
            
        Returns:
            Valor validado
            
        Raises:
            ValueError: Se o status não for válido
        """
        valid_statuses = ['success', 'error', 'pending']
        if v not in valid_statuses:
            raise ValueError(f"Status deve ser um dos seguintes: {', '.join(valid_statuses)}")
        return v

class WebhookBatchResponse(BaseModel):
    """
    Modelo para respostas de processamento em lote de webhooks.
    
    Usado quando múltiplos webhooks são processados em uma única operação.
    """
    total_processed: int = Field(
        ...,
        description="Número total de webhooks processados"
    )
    successful: int = Field(
        ...,
        description="Número de webhooks processados com sucesso"
    )
    failed: int = Field(
        ...,
        description="Número de webhooks que falharam no processamento"
    )
    results: List[WebhookResponse] = Field(
        ...,
        description="Lista de resultados individuais"
    )