# Rotas da API

Este diretório contém os roteadores FastAPI que definem os endpoints da API.

## Estrutura

Cada arquivo neste diretório define um conjunto de rotas relacionadas:

- `social_media.py` - Endpoints para gerenciamento de mídias sociais
- `webhooks.py` - Endpoints para processamento de webhooks

## Rotas Existentes

### Mídias Sociais

Endpoints para gerenciar links de mídias sociais:

- `GET /api/social-media` - Lista todas as mídias sociais
- `GET /api/social-media/{id}` - Obtém uma mídia social específica
- `POST /api/social-media` - Cria uma nova mídia social
- `PUT /api/social-media/{id}` - Atualiza uma mídia social existente
- `DELETE /api/social-media/{id}` - Remove uma mídia social

### Webhooks

Endpoints para processamento de webhooks:

- `POST /api/webhooks` - Recebe e processa webhooks
- `POST /api/webhooks/batch` - Processa múltiplos webhooks em lote
- `GET /api/webhooks/data` - Obtém dados disponíveis para webhooks

## Criando Novas Rotas

Para adicionar um novo conjunto de rotas:

1. Crie um novo arquivo Python neste diretório
2. Defina um roteador FastAPI
3. Implemente os endpoints necessários
4. Registre o roteador no arquivo `main.py`

### Exemplo Básico

```python
"""
Rotas para gerenciamento de [entidade].

Este módulo implementa endpoints para gerenciar [entidade].
"""
from fastapi import APIRouter, Depends, Path, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.modelo import Modelo
from ..schemas.schema import SchemaBase, SchemaCreate, SchemaUpdate, Schema
from ..services.database import get_db
from ..errors import BaseAPIError, NotFoundError

# Configuração do roteador
router = APIRouter()

@router.get("/", response_model=List[Schema])
async def listar_todos(
    skip: int = Query(0, description="Registros para pular"),
    limit: int = Query(100, description="Limite de registros"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros.
    
    Retorna uma lista paginada de registros.
    """
    try:
        items = db.query(Modelo).offset(skip).limit(limit).all()
        return items
    except Exception as e:
        raise BaseAPIError(
            message="Falha ao listar registros",
            status_code=500,
            details={"error": str(e)}
        )

@router.get("/{item_id}", response_model=Schema)
async def obter_por_id(
    item_id: int = Path(..., description="ID do registro"),
    db: Session = Depends(get_db)
):
    """
    Obtém um registro específico pelo ID.
    """
    try:
        item = db.query(Modelo).filter(Modelo.id == item_id).first()
        if not item:
            raise NotFoundError(f"Registro {item_id} não encontrado")
        return item
    except NotFoundError:
        raise
    except Exception as e:
        raise BaseAPIError(
            message=f"Falha ao obter registro {item_id}",
            status_code=500,
            details={"error": str(e)}
        )

@router.post("/", response_model=Schema, status_code=201)
async def criar(
    item: SchemaCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo registro.
    """
    try:
        novo_item = Modelo(**item.dict())
        db.add(novo_item)
        db.commit()
        db.refresh(novo_item)
        return novo_item
    except Exception as e:
        db.rollback()
        raise BaseAPIError(
            message="Falha ao criar registro",
            status_code=500,
            details={"error": str(e)}
        )

@router.put("/{item_id}", response_model=Schema)
async def atualizar(
    item_id: int = Path(..., description="ID do registro"),
    item: SchemaUpdate = ...,
    db: Session = Depends(get_db)
):
    """
    Atualiza um registro existente.
    """
    try:
        db_item = db.query(Modelo).filter(Modelo.id == item_id).first()
        if not db_item:
            raise NotFoundError(f"Registro {item_id} não encontrado")
            
        # Atualiza campos
        for key, value in item.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
            
        db.commit()
        db.refresh(db_item)
        return db_item
    except NotFoundError:
        raise
    except Exception as e:
        db.rollback()
        raise BaseAPIError(
            message=f"Falha ao atualizar registro {item_id}",
            status_code=500,
            details={"error": str(e)}
        )

@router.delete("/{item_id}", status_code=204)
async def remover(
    item_id: int = Path(..., description="ID do registro"),
    db: Session = Depends(get_db)
):
    """
    Remove um registro.
    """
    try:
        db_item = db.query(Modelo).filter(Modelo.id == item_id).first()
        if not db_item:
            raise NotFoundError(f"Registro {item_id} não encontrado")
            
        db.delete(db_item)
        db.commit()
        return None
    except NotFoundError:
        raise
    except Exception as e:
        db.rollback()
        raise BaseAPIError(
            message=f"Falha ao remover registro {item_id}",
            status_code=500,
            details={"error": str(e)}
        )
```

### Registrando no Aplicativo Principal

Após criar o arquivo de rotas, registre-o no aplicativo principal (`main.py`):

```python
from fastapi import FastAPI
from .routes import social_media, webhooks, nova_rota

app = FastAPI()

# Registra rotas
app.include_router(social_media.router, prefix="/api/social-media", tags=["social-media"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])
app.include_router(nova_rota.router, prefix="/api/nova-rota", tags=["nova-rota"])
```

## Boas Práticas

1. **Organização por recurso**: Cada arquivo deve corresponder a um recurso ou conjunto de recursos relacionados

2. **Documentação clara**: Use docstrings para documentar cada endpoint

3. **Tratamento de erros**: Use o framework de erros para tratamento consistente

4. **Validação com Pydantic**: Use esquemas Pydantic para validação de entrada/saída

5. **Paginação**: Implemente paginação para endpoints que retornam múltiplos itens

6. **Dependências**: Use o sistema de dependências do FastAPI para injeção de dependências

7. **Tags**: Use tags para agrupar endpoints na documentação OpenAPI

8. **Status codes**: Use códigos de status HTTP apropriados para cada operação