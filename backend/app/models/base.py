"""
Módulo base para modelos SQLAlchemy.

Define a classe Base que todos os modelos SQLAlchemy devem herdar,
além de funcionalidades comuns a todos os modelos.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, func
from datetime import datetime
from typing import Dict, Any

# Classe base para todos os modelos
Base = declarative_base()

class TimestampMixin:
    """
    Mixin para adicionar campos de timestamp a modelos.
    
    Adiciona campos created_at e updated_at que são automaticamente
    gerenciados pelo SQLAlchemy.
    """
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Data e hora de criação do registro"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Data e hora da última atualização"
    )

class ModelMixin:
    """
    Mixin com métodos úteis para todos os modelos.
    
    Adiciona funcionalidades comuns como conversão para dicionário,
    serialização e outros métodos auxiliares.
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o modelo para um dicionário.
        
        Returns:
            Dicionário com os atributos do modelo
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Atualiza o modelo a partir de um dicionário.
        
        Args:
            data: Dicionário com os novos valores
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)