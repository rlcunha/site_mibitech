# Esquemas de Dados

Este diretório contém os esquemas Pydantic que definem a estrutura de dados para entrada e saída da API.

## Visão Geral

Os esquemas Pydantic são usados para:

- Validar dados de entrada da API
- Serializar dados de saída da API
- Documentar a estrutura de dados na documentação OpenAPI
- Converter entre modelos de banco de dados e representações JSON

## Estrutura Básica

Os esquemas geralmente seguem um padrão de três camadas:

```python
from pydantic import BaseModel, Field

# Esquema base (campos comuns)
class ItemBase(BaseModel):
    nome: str = Field(..., description="Nome do item")
    descricao: str = Field(None, description="Descrição detalhada")

# Esquema para criação (sem ID)
class ItemCreate(ItemBase):
    preco: float = Field(..., gt=0, description="Preço do item")

# Esquema para resposta (com ID)
class Item(ItemBase):
    id: int = Field(..., description="ID único do item")
    preco: float
    
    class Config:
        from_attributes = True  # Permite conversão de modelos SQLAlchemy
```

## Esquemas Existentes

### SocialMedia

Esquemas para mídias sociais:

- `SocialMediaBase`: Campos comuns
- `SocialMediaCreate`: Para criação de novas mídias sociais
- `SocialMediaUpdate`: Para atualização parcial (campos opcionais)
- `SocialMediaSchema`: Para respostas da API (inclui ID)

### Webhook

Esquemas para processamento de webhooks:

- `WebhookPayload`: Dados recebidos de webhooks
- `WebhookResponse`: Resposta para confirmação de processamento
- `WebhookBatchResponse`: Resposta para processamento em lote

## Criando Novos Esquemas

### Estrutura Recomendada

```python
"""
Esquemas para [entidade].

Define os modelos de dados para validação e serialização
de informações de [entidade].
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class EntidadeBase(BaseModel):
    """
    Esquema base para [entidade].
    
    Contém campos comuns a todos os esquemas de [entidade].
    """
    nome: str = Field(
        ..., 
        description="Nome da entidade",
        min_length=1,
        max_length=100,
        example="Exemplo"
    )
    descricao: Optional[str] = Field(
        None, 
        description="Descrição detalhada",
        max_length=500,
        example="Descrição de exemplo"
    )
    
    @validator('nome')
    def nome_deve_ser_capitalizado(cls, v):
        """
        Valida e formata o nome.
        
        Args:
            v: Valor do nome
            
        Returns:
            Nome validado e formatado
        """
        return v.strip().title()

class EntidadeCreate(EntidadeBase):
    """
    Esquema para criação de [entidade].
    
    Usado para validar dados de entrada ao criar uma nova [entidade].
    """
    categoria_id: int = Field(
        ...,
        description="ID da categoria relacionada",
        gt=0,
        example=1
    )

class EntidadeUpdate(BaseModel):
    """
    Esquema para atualização de [entidade].
    
    Todos os campos são opcionais para permitir atualizações parciais.
    """
    nome: Optional[str] = Field(
        None, 
        description="Nome da entidade",
        min_length=1,
        max_length=100
    )
    descricao: Optional[str] = Field(
        None, 
        description="Descrição detalhada",
        max_length=500
    )
    categoria_id: Optional[int] = Field(
        None,
        description="ID da categoria relacionada",
        gt=0
    )
    
    @validator('nome')
    def nome_deve_ser_capitalizado(cls, v):
        if v is None:
            return v
        return v.strip().title()

class Entidade(EntidadeBase):
    """
    Esquema completo para [entidade].
    
    Usado para respostas da API, inclui todos os campos.
    """
    id: int = Field(..., description="ID único da entidade")
    categoria_id: int = Field(..., description="ID da categoria relacionada")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data da última atualização")

    class Config:
        """Configuração do Pydantic para o esquema."""
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
```

## Validação Avançada

### Validadores de Campo

Use o decorador `@validator` para validação personalizada:

```python
from pydantic import BaseModel, validator

class Usuario(BaseModel):
    email: str
    senha: str
    senha_confirmacao: str
    
    @validator('email')
    def email_valido(cls, v):
        if '@' not in v:
            raise ValueError('Email inválido')
        return v.lower()
    
    @validator('senha_confirmacao')
    def senhas_coincidem(cls, v, values):
        if 'senha' in values and v != values['senha']:
            raise ValueError('Senhas não coincidem')
        return v
```

### Validadores de Modelo

Use o método `root_validator` para validação entre campos:

```python
from pydantic import BaseModel, root_validator

class Produto(BaseModel):
    preco_normal: float
    preco_promocional: Optional[float] = None
    
    @root_validator
    def verificar_precos(cls, values):
        preco_normal = values.get('preco_normal')
        preco_promocional = values.get('preco_promocional')
        
        if preco_promocional is not None and preco_promocional >= preco_normal:
            raise ValueError('Preço promocional deve ser menor que o preço normal')
            
        return values
```

## Tipos Personalizados

Crie tipos personalizados para validação específica:

```python
from pydantic import BaseModel, constr

# String com formato específico
CpfStr = constr(regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')

class Cliente(BaseModel):
    nome: str
    cpf: CpfStr  # Validará o formato do CPF
```

## Integração com SQLAlchemy

Configure a conversão automática de modelos SQLAlchemy:

```python
from pydantic import BaseModel

class ProdutoSchema(BaseModel):
    id: int
    nome: str
    preco: float
    
    class Config:
        from_attributes = True  # Permite converter modelos SQLAlchemy
        
# Uso:
produto_db = db.query(ProdutoModel).first()
produto_schema = ProdutoSchema.from_orm(produto_db)
```

## Boas Práticas

1. **Documentação clara**: Use o parâmetro `description` para documentar campos

2. **Exemplos úteis**: Forneça exemplos realistas com o parâmetro `example`

3. **Validação robusta**: Implemente validadores para garantir integridade dos dados

4. **Esquemas específicos**: Crie esquemas diferentes para diferentes operações (criar, atualizar, responder)

5. **Campos opcionais para atualizações**: Use `Optional` para permitir atualizações parciais

6. **Consistência de nomenclatura**: Siga um padrão consistente para nomes de esquemas

7. **Reutilização de código**: Use esquemas base para campos comuns

8. **Validação em camadas**: Combine validação de esquema com validação de modelo