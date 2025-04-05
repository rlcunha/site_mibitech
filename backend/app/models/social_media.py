"""
Modelo para mídias sociais.

Define a estrutura da tabela de mídias sociais no banco de dados
e métodos relacionados.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from typing import Dict, Any

from .base import Base, TimestampMixin, ModelMixin
from ..helpers import StringProcessor
from ..errors import ValidationError

class SocialMedia(Base, TimestampMixin, ModelMixin):
    """
    Modelo para armazenar informações de mídias sociais.
    
    Representa links para perfis de mídias sociais exibidos no site.
    Herda TimestampMixin para campos de data/hora automáticos e
    ModelMixin para métodos utilitários comuns.
    """
    __tablename__ = "social_media"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True,
                 comment="Nome da plataforma de mídia social")
    url = Column(String(255), nullable=False,
                comment="URL completa para o perfil na mídia social")
    icon = Column(String(50), nullable=False,
                 comment="Nome do ícone para exibição (ex: 'facebook', 'twitter')")

    @validates('name', 'url', 'icon')
    def validate_fields(self, key: str, value: str) -> str:
        """
        Valida campos do modelo durante atribuição.
        
        Este método é chamado automaticamente pelo SQLAlchemy
        quando valores são atribuídos aos campos.
        
        Args:
            key: Nome do campo sendo validado
            value: Valor sendo atribuído
            
        Returns:
            Valor validado
            
        Raises:
            ValidationError: Se o valor for inválido
        """
        # Inicializa processadores
        string_processor = StringProcessor()
        
        # Validações específicas por campo
        if key == 'name':
            if not string_processor.validate(value) or len(value) > 100:
                raise ValidationError(
                    message="Nome de mídia social inválido",
                    details={"name": value, "reason": "Nome vazio ou muito longo"}
                )
        elif key == 'url':
            if not string_processor.validate_url(value):
                raise ValidationError(
                    message="URL de mídia social inválida",
                    details={"url": value, "reason": "Formato de URL inválido"}
                )
        elif key == 'icon':
            if not string_processor.validate(value) or len(value) > 50:
                raise ValidationError(
                    message="Nome de ícone inválido",
                    details={"icon": value, "reason": "Nome vazio ou muito longo"}
                )
                
        return value

    def validate(self) -> bool:
        """
        Valida todos os dados do modelo usando o framework de helpers.
        
        Útil para validação completa antes de operações de banco de dados.
        
        Returns:
            bool: True se todos os dados são válidos
            
        Raises:
            ValidationError: Se algum dado for inválido
        """
        validator = StringProcessor()
        
        # Valida cada campo
        validations = [
            validator.validate(self.name),
            validator.validate_url(self.url),
            validator.validate(self.icon)
        ]
        
        if not all(validations):
            raise ValidationError(
                message="Dados de mídia social inválidos",
                details={
                    "name": self.name,
                    "url": self.url,
                    "icon": self.icon
                }
            )
            
        return True
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o modelo para um dicionário.
        
        Útil para serialização e APIs.
        
        Returns:
            Dicionário representando o modelo
        """
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "icon": self.icon,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }