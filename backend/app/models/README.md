# Modelos de Dados

Este diretório contém os modelos SQLAlchemy que representam as entidades do banco de dados.

## Visão Geral

Os modelos definem:

- Estrutura das tabelas do banco de dados
- Relacionamentos entre entidades
- Validações em nível de modelo
- Métodos auxiliares para manipulação de dados

## Estrutura Base

Todos os modelos herdam de `Base` e podem usar os mixins disponíveis:

```python
from .base import Base, TimestampMixin, ModelMixin

class MeuModelo(Base, TimestampMixin, ModelMixin):
    __tablename__ = "minha_tabela"
    
    id = Column(Integer, primary_key=True)
    # ...
```

### Mixins Disponíveis

- **TimestampMixin**: Adiciona campos `created_at` e `updated_at` que são gerenciados automaticamente
- **ModelMixin**: Adiciona métodos utilitários como `to_dict()` e `update_from_dict()`

## Modelos Existentes

### SocialMedia

Representa links para redes sociais exibidos no site.

```python
class SocialMedia(Base, TimestampMixin, ModelMixin):
    __tablename__ = "social_media"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    url = Column(String(255), nullable=False)
    icon = Column(String(50), nullable=False)
```

## Definindo Novos Modelos

### Estrutura Recomendada

```python
"""
Modelo para [entidade].

Define a estrutura da tabela [entidade] no banco de dados
e métodos relacionados.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, validates
from typing import Dict, Any, List

from .base import Base, TimestampMixin, ModelMixin
from ..helpers import StringProcessor
from ..errors import ValidationError

class NomeModelo(Base, TimestampMixin, ModelMixin):
    """
    Modelo para armazenar informações de [entidade].
    
    [Descrição detalhada do propósito e uso do modelo]
    """
    __tablename__ = "nome_tabela"

    # Colunas primárias
    id = Column(Integer, primary_key=True, index=True)
    
    # Colunas de dados
    nome = Column(String(100), nullable=False, 
                 comment="Nome da entidade")
    descricao = Column(String(500), nullable=True,
                      comment="Descrição detalhada")
    ativo = Column(Boolean, default=True,
                  comment="Status de ativação")
    
    # Relacionamentos
    itens = relationship("Item", back_populates="nome_modelo")
    
    # Validadores
    @validates('nome', 'descricao')
    def validate_fields(self, key: str, value: str) -> str:
        """
        Valida campos do modelo durante atribuição.
        
        Args:
            key: Nome do campo sendo validado
            value: Valor sendo atribuído
            
        Returns:
            Valor validado
            
        Raises:
            ValidationError: Se o valor for inválido
        """
        string_processor = StringProcessor()
        
        if key == 'nome':
            if not string_processor.validate(value) or len(value) > 100:
                raise ValidationError(
                    message="Nome inválido",
                    details={"nome": value, "reason": "Nome vazio ou muito longo"}
                )
                
        return value
    
    # Métodos adicionais
    def alguma_operacao(self) -> Any:
        """
        [Descrição da operação]
        
        Returns:
            [Descrição do retorno]
        """
        # Implementação
        pass
```

## Relacionamentos

### Um para Muitos

```python
# Lado "um"
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    
    # Relacionamento
    posts = relationship("Post", back_populates="usuario")

# Lado "muitos"
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    
    # Chave estrangeira
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    
    # Relacionamento
    usuario = relationship("Usuario", back_populates="posts")
```

### Muitos para Muitos

```python
# Tabela de associação
produto_categoria = Table(
    "produto_categoria",
    Base.metadata,
    Column("produto_id", Integer, ForeignKey("produtos.id"), primary_key=True),
    Column("categoria_id", Integer, ForeignKey("categorias.id"), primary_key=True)
)

class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    
    # Relacionamento
    categorias = relationship("Categoria", secondary=produto_categoria, 
                             back_populates="produtos")

class Categoria(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    
    # Relacionamento
    produtos = relationship("Produto", secondary=produto_categoria, 
                           back_populates="categorias")
```

## Validação de Dados

Use o decorador `@validates` para validar dados durante a atribuição:

```python
from sqlalchemy.orm import validates
from ..errors import ValidationError

class Produto(Base):
    # ...
    preco = Column(Numeric(10, 2))
    
    @validates('preco')
    def validate_preco(self, key, value):
        if value <= 0:
            raise ValidationError("Preço deve ser maior que zero")
        return value
```

## Métodos Auxiliares

Implemente métodos auxiliares para operações comuns:

```python
def to_dict(self) -> Dict[str, Any]:
    """Converte o modelo para um dicionário."""
    return {
        "id": self.id,
        "nome": self.nome,
        # ...
    }

def from_dict(self, data: Dict[str, Any]) -> None:
    """Atualiza o modelo a partir de um dicionário."""
    for key, value in data.items():
        if hasattr(self, key):
            setattr(self, key, value)
```

## Boas Práticas

1. **Nomeação consistente**: Use nomes de tabelas no singular e em snake_case

2. **Comentários nas colunas**: Documente o propósito de cada coluna

3. **Validação em múltiplas camadas**: Valide dados no modelo, schema e serviço

4. **Tipos apropriados**: Use os tipos SQLAlchemy mais adequados para cada dado

5. **Índices estratégicos**: Adicione índices em colunas frequentemente consultadas

6. **Relacionamentos bem definidos**: Configure corretamente cascade, lazy loading, etc.

7. **Evite lógica de negócio complexa**: Mantenha os modelos focados em persistência

8. **Documente relacionamentos**: Explique a natureza das relações entre entidades