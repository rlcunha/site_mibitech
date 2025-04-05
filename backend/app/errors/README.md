# Framework de Tratamento de Erros

Este framework fornece uma estrutura padronizada para gerenciamento de exceções e erros na aplicação.

## Visão Geral

O framework de erros é projetado para:

- Padronizar respostas de erro da API
- Centralizar o tratamento de exceções
- Facilitar o logging e monitoramento
- Melhorar a experiência do desenvolvedor e do usuário

## Classes de Erro

### BaseAPIError

Classe base para todos os erros da API.

```python
from app.errors import BaseAPIError

# Criar um erro básico
raise BaseAPIError(
    message="Ocorreu um erro",
    status_code=500,
    details={"campo": "valor"}
)
```

### Erros Específicos

O framework inclui classes para tipos comuns de erros:

#### ValidationError

Para erros de validação de dados.

```python
from app.errors import ValidationError

# Erro de validação
raise ValidationError(
    message="Dados inválidos",
    details={"campo": "O campo é obrigatório"}
)
```

#### DatabaseError

Para erros relacionados ao banco de dados.

```python
from app.errors import DatabaseError

# Erro de banco de dados
raise DatabaseError(
    message="Falha na operação do banco de dados",
    details={"operacao": "insert", "tabela": "usuarios"}
)
```

#### NotFoundError

Para recursos não encontrados.

```python
from app.errors import NotFoundError

# Recurso não encontrado
raise NotFoundError(
    message="Usuário não encontrado",
    details={"id": 123}
)
```

#### AuthenticationError

Para falhas de autenticação.

```python
from app.errors import AuthenticationError

# Erro de autenticação
raise AuthenticationError(
    message="Credenciais inválidas",
    details={"motivo": "Token expirado"}
)
```

## Manipulador de Erros

O framework inclui um manipulador central de erros que converte exceções em respostas HTTP apropriadas.

### Registro Automático

Todos os erros são automaticamente registrados no log com detalhes relevantes:

- Timestamp
- Tipo de erro
- Mensagem
- Detalhes adicionais
- Stack trace (para erros não tratados)

### Formato de Resposta

Todas as respostas de erro seguem um formato consistente:

```json
{
  "error": {
    "message": "Mensagem descritiva do erro",
    "code": 400,
    "timestamp": "2025-04-05T10:38:00.000Z",
    "details": {
      "campo": "informação adicional"
    }
  }
}
```

## Uso Recomendado

### Em Rotas da API

```python
@router.get("/{item_id}")
async def get_item(item_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise NotFoundError(f"Item com ID {item_id} não encontrado")
        return item
    except SQLAlchemyError as e:
        raise DatabaseError("Erro ao buscar item", details={"error": str(e)})
```

### Em Serviços

```python
def processar_pagamento(pagamento):
    try:
        # Lógica de processamento
        if pagamento.valor <= 0:
            raise ValidationError("Valor de pagamento inválido")
        # ...
    except ExternalAPIError as e:
        raise BaseAPIError("Falha no gateway de pagamento", status_code=502)
```

### Registro de Erros Personalizado

```python
from app.errors import BaseAPIError
import logging

logger = logging.getLogger("meu_modulo")

try:
    # Operação arriscada
except Exception as e:
    logger.error(f"Erro específico: {str(e)}")
    raise BaseAPIError("Ocorreu um erro na operação", log_error=False)  # Evita log duplicado
```

## Integração com FastAPI

O framework se integra automaticamente com o FastAPI através da função `register_error_handlers`:

```python
from fastapi import FastAPI
from app.errors import register_error_handlers

app = FastAPI()
register_error_handlers(app)
```

## Boas Práticas

1. **Use erros específicos**: Prefira classes específicas como `ValidationError` em vez da genérica `BaseAPIError`

2. **Mensagens claras**: Forneça mensagens de erro descritivas e úteis

3. **Detalhes apropriados**: Inclua detalhes relevantes, mas evite expor informações sensíveis

4. **Tratamento em camadas**: Capture exceções no nível mais apropriado da aplicação

5. **Consistência**: Mantenha um padrão consistente de tratamento de erros em toda a aplicação