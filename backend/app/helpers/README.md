# Framework de Helpers

Este framework fornece classes e utilitários para processamento, validação e transformação de dados na aplicação.

## Visão Geral

O framework de helpers é projetado para padronizar operações comuns de dados, como:

- Validação de dados
- Transformação de formatos
- Normalização de estruturas
- Processamento de tipos específicos (strings, JSON, datas)

## Classes Principais

### DataProcessor

Classe base para todas as operações de processamento de dados.

```python
from app.helpers import DataProcessor

class MeuProcessador(DataProcessor):
    def process(self, data):
        # Implementação personalizada
        return data_processado
        
    def validate(self, data):
        # Lógica de validação
        return True  # ou False
```

### StringProcessor

Processador especializado para manipulação de strings.

```python
from app.helpers import StringProcessor

processor = StringProcessor()

# Validar email
if processor.validate_email("usuario@exemplo.com"):
    # Email válido
    
# Validar URL
if processor.validate_url("https://mibitech.com"):
    # URL válida
```

### JsonProcessor

Processador especializado para dados JSON.

```python
from app.helpers import JsonProcessor

processor = JsonProcessor()

# Processar JSON
try:
    data = processor.process('{"nome": "MibiTech", "ano": 2025}')
    # data é um dicionário Python
except ValueError:
    # JSON inválido
    
# Converter para string JSON formatada
json_str = processor.to_json_string(data)
```

### DateTimeProcessor

Processador para manipulação de datas e horas.

```python
from app.helpers import DateTimeProcessor
from datetime import datetime

processor = DateTimeProcessor()

# Processar string de data
data = processor.process("2025-04-05")  # Retorna objeto datetime

# Formatar data
data_formatada = processor.format_datetime(datetime.now(), "%d/%m/%Y")
```

## Uso Recomendado

1. **Validação de Entrada**: Use os processadores para validar dados de entrada em APIs.

```python
@router.post("/")
async def criar_item(item: ItemSchema):
    processor = StringProcessor()
    if not processor.validate(item.nome):
        raise ValidationError("Nome inválido")
    # ...
```

2. **Transformação de Dados**: Padronize a transformação de dados entre camadas.

```python
def get_dados_formatados():
    dados = obter_dados_brutos()
    processor = JsonProcessor()
    return processor.process(dados)
```

3. **Extensão para Casos Específicos**: Crie processadores personalizados para lógicas de negócio.

```python
class ProdutoProcessor(DataProcessor):
    def validate(self, produto):
        # Validação específica para produtos
        return produto.preco > 0 and len(produto.nome) > 3
```

## Boas Práticas

- Prefira usar os processadores existentes antes de criar novos
- Mantenha a responsabilidade única para cada processador
- Documente comportamentos específicos em processadores personalizados
- Use validação em camadas (API, serviço, modelo) para garantir integridade dos dados