"""
Esquemas para mídias sociais.

Define os modelos de dados para validação e serialização
de informações de mídias sociais.
"""
from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Optional
from datetime import datetime

class SocialMediaBase(BaseModel):
    """
    Esquema base para mídias sociais.
    
    Contém campos comuns a todos os esquemas de mídia social.
    """
    name: str = Field(
        ...,
        description="Nome da plataforma de mídia social",
        min_length=1,
        max_length=100,
        example="Facebook"
    )
    url: str = Field(
        ...,
        description="URL completa para o perfil na mídia social",
        example="https://facebook.com/mibitech"
    )
    icon: str = Field(
        ...,
        description="Nome do ícone para exibição",
        min_length=1,
        max_length=50,
        example="facebook"
    )
    
    @validator('url')
    def validate_url(cls, v):
        """
        Valida se a URL está em formato correto.
        
        Args:
            v: Valor da URL
            
        Returns:
            URL validada
            
        Raises:
            ValueError: Se a URL for inválida
        """
        # Tenta validar como HttpUrl
        try:
            HttpUrl(v)
        except Exception:
            raise ValueError("URL inválida")
        return v

class SocialMediaCreate(SocialMediaBase):
    """
    Esquema para criação de mídia social.
    
    Usado para validar dados de entrada ao criar uma nova mídia social.
    """
    pass

class SocialMediaUpdate(BaseModel):
    """
    Esquema para atualização de mídia social.
    
    Todos os campos são opcionais para permitir atualizações parciais.
    """
    name: Optional[str] = Field(
        None,
        description="Nome da plataforma de mídia social",
        min_length=1,
        max_length=100
    )
    url: Optional[str] = Field(
        None,
        description="URL completa para o perfil na mídia social"
    )
    icon: Optional[str] = Field(
        None,
        description="Nome do ícone para exibição",
        min_length=1,
        max_length=50
    )
    
    @validator('url')
    def validate_url(cls, v):
        """
        Valida URL se fornecida.
        
        Args:
            v: Valor da URL
            
        Returns:
            URL validada ou None
            
        Raises:
            ValueError: Se a URL for inválida
        """
        if v is None:
            return v
            
        try:
            HttpUrl(v)
        except Exception:
            raise ValueError("URL inválida")
        return v

class SocialMediaSchema(SocialMediaBase):
    """
    Esquema completo para mídia social.
    
    Usado para respostas da API, inclui todos os campos do modelo.
    """
    id: int = Field(..., description="ID único da mídia social")
    created_at: Optional[datetime] = Field(
        None,
        description="Data e hora de criação do registro"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Data e hora da última atualização"
    )

    class Config:
        """Configuração do Pydantic para o esquema."""
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat() if dt else None
        }