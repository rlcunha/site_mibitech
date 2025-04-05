"""
Framework de ajuda para processamento e transformação de dados.

Fornece classes base e utilitários para:
- Validação de dados
- Transformação de dados
- Normalização de dados
- Operações comuns de dados
"""
from typing import Any, Dict, Optional, List, Union
import re
import json
from datetime import datetime

class DataProcessor:
    """
    Classe base para operações de processamento de dados.
    
    Esta classe define a interface básica que todas as classes de processamento
    de dados devem implementar. Serve como um contrato para garantir consistência
    em todo o sistema.
    """
    
    def process(self, data: Any) -> Any:
        """
        Processa os dados de entrada.
        
        Args:
            data: Dados a serem processados
            
        Returns:
            Dados processados
            
        Raises:
            NotImplementedError: Se a subclasse não implementar este método
        """
        raise NotImplementedError("Subclasses devem implementar process()")

    def validate(self, data: Any) -> bool:
        """
        Valida os dados de entrada.
        
        Args:
            data: Dados a serem validados
            
        Returns:
            bool: True se os dados são válidos, False caso contrário
            
        Raises:
            NotImplementedError: Se a subclasse não implementar este método
        """
        raise NotImplementedError("Subclasses devem implementar validate()")

class DataTransformer(DataProcessor):
    """
    Classe base para operações de transformação de dados.
    
    Estende DataProcessor para fornecer funcionalidade específica
    para transformação de dados de um formato para outro.
    """
    
    def transform(self, data: Any) -> Any:
        """
        Transforma os dados de entrada.
        
        Esta é uma implementação padrão que chama o método process().
        Subclasses podem sobrescrever este método para comportamento personalizado.
        
        Args:
            data: Dados a serem transformados
            
        Returns:
            Dados transformados
        """
        return self.process(data)
    
    def batch_transform(self, items: List[Any]) -> List[Any]:
        """
        Transforma uma lista de itens.
        
        Args:
            items: Lista de itens a serem transformados
            
        Returns:
            Lista de itens transformados
        """
        return [self.transform(item) for item in items]

class DataNormalizer(DataProcessor):
    """
    Classe base para operações de normalização de dados.
    
    Especializada em converter dados de vários formatos para
    um formato padrão consistente, geralmente um dicionário.
    """
    
    def normalize(self, data: Any) -> Dict[str, Any]:
        """
        Normaliza os dados de entrada em um formato padrão.
        
        Args:
            data: Dados a serem normalizados
            
        Returns:
            Dicionário contendo os dados normalizados
        """
        processed = self.process(data)
        return self._to_dict(processed)
    
    def _to_dict(self, data: Any) -> Dict[str, Any]:
        """
        Converte dados processados para formato de dicionário.
        
        Args:
            data: Dados a serem convertidos
            
        Returns:
            Dicionário representando os dados
            
        Raises:
            NotImplementedError: Se a subclasse não implementar este método
        """
        raise NotImplementedError("Subclasses devem implementar _to_dict()")

class StringProcessor(DataProcessor):
    """
    Processador especializado para manipulação de strings.
    
    Fornece métodos úteis para validação e transformação de strings.
    """
    
    def process(self, data: str) -> str:
        """
        Processa uma string (implementação padrão retorna a mesma string).
        
        Args:
            data: String a ser processada
            
        Returns:
            String processada
        """
        if not isinstance(data, str):
            return str(data)
        return data.strip()
    
    def validate(self, data: Any) -> bool:
        """
        Valida se o dado é uma string não vazia.
        
        Args:
            data: Dado a ser validado
            
        Returns:
            bool: True se for uma string não vazia, False caso contrário
        """
        if not isinstance(data, str):
            return False
        return len(data.strip()) > 0
    
    def validate_email(self, email: str) -> bool:
        """
        Valida se uma string é um endereço de email válido.
        
        Args:
            email: String a ser validada como email
            
        Returns:
            bool: True se for um email válido, False caso contrário
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_url(self, url: str) -> bool:
        """
        Valida se uma string é uma URL válida.
        
        Args:
            url: String a ser validada como URL
            
        Returns:
            bool: True se for uma URL válida, False caso contrário
        """
        pattern = r'^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        return bool(re.match(pattern, url))

class JsonProcessor(DataProcessor):
    """
    Processador especializado para manipulação de dados JSON.
    
    Fornece métodos para validação, parsing e transformação de JSON.
    """
    
    def process(self, data: Union[str, Dict, List]) -> Dict:
        """
        Processa dados JSON, garantindo que sejam convertidos para dicionário.
        
        Args:
            data: Dados JSON como string ou já como objeto Python
            
        Returns:
            Dicionário Python representando os dados JSON
            
        Raises:
            ValueError: Se os dados não puderem ser processados como JSON
        """
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string")
        elif isinstance(data, (dict, list)):
            return data
        else:
            raise ValueError("Data must be JSON string, dict, or list")
    
    def validate(self, data: Any) -> bool:
        """
        Valida se os dados são JSON válido.
        
        Args:
            data: Dados a serem validados
            
        Returns:
            bool: True se os dados são JSON válido, False caso contrário
        """
        if isinstance(data, (dict, list)):
            return True
        
        if not isinstance(data, str):
            return False
            
        try:
            json.loads(data)
            return True
        except (json.JSONDecodeError, TypeError):
            return False
    
    def to_json_string(self, data: Any) -> str:
        """
        Converte dados para uma string JSON formatada.
        
        Args:
            data: Dados a serem convertidos
            
        Returns:
            String JSON formatada
        """
        return json.dumps(data, indent=2, ensure_ascii=False)

class DateTimeProcessor(DataProcessor):
    """
    Processador especializado para manipulação de datas e horas.
    
    Fornece métodos para validação e transformação de dados temporais.
    """
    
    def process(self, data: Union[str, datetime]) -> datetime:
        """
        Processa dados de data/hora para objeto datetime.
        
        Args:
            data: String de data/hora ou objeto datetime
            
        Returns:
            Objeto datetime
            
        Raises:
            ValueError: Se os dados não puderem ser convertidos para datetime
        """
        if isinstance(data, datetime):
            return data
            
        if isinstance(data, str):
            try:
                # Tenta vários formatos comuns
                for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                    try:
                        return datetime.strptime(data, fmt)
                    except ValueError:
                        continue
                raise ValueError(f"Unsupported datetime format: {data}")
            except ValueError:
                raise ValueError(f"Invalid datetime string: {data}")
                
        raise ValueError("Data must be datetime object or string")
    
    def validate(self, data: Any) -> bool:
        """
        Valida se os dados representam uma data/hora válida.
        
        Args:
            data: Dados a serem validados
            
        Returns:
            bool: True se os dados são uma data/hora válida, False caso contrário
        """
        if isinstance(data, datetime):
            return True
            
        if not isinstance(data, str):
            return False
            
        try:
            self.process(data)
            return True
        except ValueError:
            return False
    
    def format_datetime(self, dt: Union[str, datetime], output_format: str = "%Y-%m-%dT%H:%M:%S") -> str:
        """
        Formata um objeto datetime ou string para o formato especificado.
        
        Args:
            dt: Objeto datetime ou string de data/hora
            output_format: Formato de saída desejado
            
        Returns:
            String formatada de data/hora
        """
        if isinstance(dt, str):
            dt = self.process(dt)
        return dt.strftime(output_format)