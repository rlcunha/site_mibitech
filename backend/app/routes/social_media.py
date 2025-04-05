"""
Rotas para gerenciamento de mídias sociais.

Este módulo implementa endpoints para gerenciar informações
de mídias sociais exibidas no site.
"""
from fastapi import APIRouter, Depends, Path, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
import logging

from ..models.social_media import SocialMedia
from ..services.database import get_db
from ..schemas.social_media import SocialMediaSchema, SocialMediaCreate, SocialMediaUpdate
from ..errors import BaseAPIError, NotFoundError, ValidationError, DatabaseError
from ..helpers import DataProcessor, StringProcessor

# Configuração de logging
logger = logging.getLogger("api.social_media")

router = APIRouter()

@router.get("/", response_model=List[SocialMediaSchema])
async def get_social_media(
    skip: int = Query(0, description="Número de registros para pular"),
    limit: int = Query(100, description="Número máximo de registros para retornar"),
    db: Session = Depends(get_db)
):
    """
    Obtém todas as mídias sociais.
    
    Retorna uma lista paginada de links de mídias sociais.
    
    Args:
        skip: Número de registros para pular (paginação)
        limit: Número máximo de registros para retornar
        db: Sessão do banco de dados
        
    Returns:
        Lista de objetos SocialMediaSchema
    """
    try:
        # Busca dados com paginação
        social_media = db.query(SocialMedia).offset(skip).limit(limit).all()
        
        # Processa e valida dados
        string_processor = StringProcessor()
        for item in social_media:
            # Valida URLs
            if not string_processor.validate_url(item.url):
                logger.warning(f"URL inválida encontrada: {item.url}")
                
        return social_media
        
    except SQLAlchemyError as e:
        # Erro específico de banco de dados
        logger.error(f"Erro de banco de dados: {str(e)}")
        raise DatabaseError(
            message="Falha ao buscar links de mídias sociais",
            details={"error": str(e)}
        )
    except Exception as e:
        # Outros erros
        logger.error(f"Erro ao buscar mídias sociais: {str(e)}", exc_info=True)
        raise BaseAPIError(
            message="Falha ao buscar links de mídias sociais",
            status_code=500,
            details={"error": str(e)}
        )

@router.post("/", response_model=SocialMediaSchema, status_code=201)
async def create_social_media(
    social_media: SocialMediaCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova mídia social.
    
    Args:
        social_media: Dados da mídia social a ser criada
        db: Sessão do banco de dados
        
    Returns:
        Objeto SocialMediaSchema criado
    """
    try:
        # Valida dados de entrada
        string_processor = StringProcessor()
        if not string_processor.validate_url(social_media.url):
            raise ValidationError(
                message="URL de mídia social inválida",
                details={"url": social_media.url}
            )
            
        # Verifica se já existe com o mesmo nome
        existing = db.query(SocialMedia).filter(SocialMedia.name == social_media.name).first()
        if existing:
            raise ValidationError(
                message="Mídia social com este nome já existe",
                details={"name": social_media.name}
            )
            
        # Cria novo registro
        db_social_media = SocialMedia(
            name=social_media.name,
            url=social_media.url,
            icon=social_media.icon
        )
        
        db.add(db_social_media)
        db.commit()
        db.refresh(db_social_media)
        
        logger.info(f"Mídia social criada: {social_media.name}")
        return db_social_media
        
    except ValidationError as e:
        # Re-lança erros de validação
        raise e
    except SQLAlchemyError as e:
        # Erro de banco de dados
        db.rollback()
        logger.error(f"Erro de banco de dados ao criar mídia social: {str(e)}")
        raise DatabaseError(
            message="Falha ao criar mídia social",
            details={"error": str(e)}
        )
    except Exception as e:
        # Outros erros
        db.rollback()
        logger.error(f"Erro ao criar mídia social: {str(e)}", exc_info=True)
        raise BaseAPIError(
            message="Falha ao criar mídia social",
            status_code=500,
            details={"error": str(e)}
        )

@router.get("/{social_media_id}", response_model=SocialMediaSchema)
async def get_social_media_by_id(
    social_media_id: int = Path(..., description="ID da mídia social"),
    db: Session = Depends(get_db)
):
    """
    Obtém uma mídia social pelo ID.
    
    Args:
        social_media_id: ID da mídia social a buscar
        db: Sessão do banco de dados
        
    Returns:
        Objeto SocialMediaSchema
        
    Raises:
        NotFoundError: Se a mídia social não for encontrada
    """
    try:
        social_media = db.query(SocialMedia).filter(SocialMedia.id == social_media_id).first()
        
        if not social_media:
            raise NotFoundError(
                message=f"Mídia social com ID {social_media_id} não encontrada"
            )
            
        return social_media
        
    except NotFoundError as e:
        # Re-lança erro de não encontrado
        raise e
    except Exception as e:
        logger.error(f"Erro ao buscar mídia social por ID: {str(e)}")
        raise BaseAPIError(
            message="Falha ao buscar mídia social",
            status_code=500,
            details={"error": str(e)}
        )

@router.put("/{social_media_id}", response_model=SocialMediaSchema)
async def update_social_media(
    social_media_id: int = Path(..., description="ID da mídia social"),
    social_media: SocialMediaUpdate = ...,
    db: Session = Depends(get_db)
):
    """
    Atualiza uma mídia social existente.
    
    Args:
        social_media_id: ID da mídia social a atualizar
        social_media: Dados atualizados
        db: Sessão do banco de dados
        
    Returns:
        Objeto SocialMediaSchema atualizado
        
    Raises:
        NotFoundError: Se a mídia social não for encontrada
    """
    try:
        # Busca registro existente
        db_social_media = db.query(SocialMedia).filter(SocialMedia.id == social_media_id).first()
        
        if not db_social_media:
            raise NotFoundError(
                message=f"Mídia social com ID {social_media_id} não encontrada"
            )
            
        # Valida URL se fornecida
        if social_media.url:
            string_processor = StringProcessor()
            if not string_processor.validate_url(social_media.url):
                raise ValidationError(
                    message="URL de mídia social inválida",
                    details={"url": social_media.url}
                )
                
        # Atualiza campos
        if social_media.name:
            db_social_media.name = social_media.name
        if social_media.url:
            db_social_media.url = social_media.url
        if social_media.icon:
            db_social_media.icon = social_media.icon
            
        db.commit()
        db.refresh(db_social_media)
        
        logger.info(f"Mídia social atualizada: ID {social_media_id}")
        return db_social_media
        
    except (NotFoundError, ValidationError) as e:
        # Re-lança erros específicos
        raise e
    except SQLAlchemyError as e:
        # Erro de banco de dados
        db.rollback()
        logger.error(f"Erro de banco de dados ao atualizar mídia social: {str(e)}")
        raise DatabaseError(
            message="Falha ao atualizar mídia social",
            details={"error": str(e)}
        )
    except Exception as e:
        # Outros erros
        db.rollback()
        logger.error(f"Erro ao atualizar mídia social: {str(e)}", exc_info=True)
        raise BaseAPIError(
            message="Falha ao atualizar mídia social",
            status_code=500,
            details={"error": str(e)}
        )

@router.delete("/{social_media_id}", status_code=204)
async def delete_social_media(
    social_media_id: int = Path(..., description="ID da mídia social"),
    db: Session = Depends(get_db)
):
    """
    Remove uma mídia social.
    
    Args:
        social_media_id: ID da mídia social a remover
        db: Sessão do banco de dados
        
    Returns:
        Resposta vazia com status 204
        
    Raises:
        NotFoundError: Se a mídia social não for encontrada
    """
    try:
        # Busca registro existente
        db_social_media = db.query(SocialMedia).filter(SocialMedia.id == social_media_id).first()
        
        if not db_social_media:
            raise NotFoundError(
                message=f"Mídia social com ID {social_media_id} não encontrada"
            )
            
        # Remove registro
        db.delete(db_social_media)
        db.commit()
        
        logger.info(f"Mídia social removida: ID {social_media_id}")
        return None
        
    except NotFoundError as e:
        # Re-lança erro de não encontrado
        raise e
    except SQLAlchemyError as e:
        # Erro de banco de dados
        db.rollback()
        logger.error(f"Erro de banco de dados ao remover mídia social: {str(e)}")
        raise DatabaseError(
            message="Falha ao remover mídia social",
            details={"error": str(e)}
        )
    except Exception as e:
        # Outros erros
        db.rollback()
        logger.error(f"Erro ao remover mídia social: {str(e)}", exc_info=True)
        raise BaseAPIError(
            message="Falha ao remover mídia social",
            status_code=500,
            details={"error": str(e)}
        )