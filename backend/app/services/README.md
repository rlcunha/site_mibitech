# Serviços da Aplicação

Este diretório contém os serviços que implementam a lógica de negócio da aplicação.

## Serviço de Banco de Dados

O arquivo `database.py` implementa a conexão com o banco de dados PostgreSQL:

```python
# Obter uma sessão de banco de dados
from app.services.database import get_db

@router.get("/items")
async def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items
```

### Principais Funcionalidades

- Configuração da conexão com PostgreSQL
- Pool de conexões para melhor performance
- Validação de parâmetros de conexão
- Tratamento de erros de banco de dados
- Monitoramento de conexões

### Como Usar

1. Importe a função `get_db` para obter uma sessão:

```python
from app.services.database import get_db
from sqlalchemy.orm import Session

# Como dependência em rotas FastAPI
@router.get("/")
def read_items(db: Session = Depends(get_db)):
    # Use a sessão aqui
    return db.query(Item).all()
```

2. Para estatísticas do pool de conexões:

```python
from app.services.database import get_engine_stats

stats = get_engine_stats()
print(f"Conexões ativas: {stats['checkedout']}")
```

## Criando Novos Serviços

Para criar um novo serviço:

1. Crie um arquivo Python no diretório `services/`
2. Implemente a lógica de negócio em classes ou funções
3. Use injeção de dependências para receber a sessão do banco de dados
4. Trate erros adequadamente usando o framework de erros

Exemplo básico:

```python
from sqlalchemy.orm import Session
from ..errors import NotFoundError

class ItemService:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, item_id: int):
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise NotFoundError(f"Item {item_id} não encontrado")
        return item
