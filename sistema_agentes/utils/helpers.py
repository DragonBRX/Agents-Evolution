"""
Funções utilitárias auxiliares.
"""

import hashlib
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, TypeVar

T = TypeVar('T')


def generate_id(prefix: str = "", length: int = 16) -> str:
    """Gera um ID único baseado em hash."""
    data = f"{prefix}_{time.time()}_{random_string(8)}"
    return hashlib.sha256(data.encode()).hexdigest()[:length]


def random_string(length: int = 8) -> str:
    """Gera uma string aleatória."""
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def timestamp_now() -> float:
    """Retorna timestamp atual."""
    return time.time()


def format_timestamp(ts: float, formato: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Formata um timestamp para string."""
    return datetime.fromtimestamp(ts).strftime(formato)


def format_duration(seconds: float) -> str:
    """Formata duração em segundos para string legível."""
    td = timedelta(seconds=int(seconds))
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def sanitize_filename(filename: str) -> str:
    """Sanitiza um nome de arquivo."""
    # Remove caracteres inválidos
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove espaços múltiplos
    sanitized = re.sub(r'\s+', '_', sanitized)
    # Limita tamanho
    return sanitized[:255]


def chunk_list(lst: List[T], chunk_size: int) -> List[List[T]]:
    """Divide uma lista em chunks de tamanho especificado."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Mescla dois dicionários, com override tendo prioridade."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Trunca um texto para o tamanho máximo especificado."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def count_tokens(text: str) -> int:
    """Estima número de tokens (palavras aproximadas)."""
    return len(text.split())


def calculate_similarity(str1: str, str2: str) -> float:
    """Calcula similaridade entre duas strings (0-1)."""
    from difflib import SequenceMatcher
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def extract_keywords(text: str, min_length: int = 4, max_keywords: int = 20) -> List[str]:
    """Extrai palavras-chave de um texto."""
    # Remove pontuação e converte para minúsculas
    words = re.findall(r'\b[a-zA-Z]{' + str(min_length) + ',}\b', text.lower())
    
    # Conta frequência
    from collections import Counter
    word_counts = Counter(words)
    
    # Remove palavras comuns (stopwords simples)
    stopwords = {'this', 'that', 'with', 'from', 'they', 'have', 'been', 'their', 'were'}
    for stop in stopwords:
        word_counts.pop(stop, None)
    
    # Retorna as mais frequentes
    return [word for word, _ in word_counts.most_common(max_keywords)]


def ensure_dir(path: Path) -> Path:
    """Garante que um diretório existe."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_json_loads(data: str, default: Any = None) -> Any:
    """Carrega JSON de forma segura."""
    import json
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(data: Any, default: str = "{}") -> str:
    """Serializa para JSON de forma segura."""
    import json
    try:
        return json.dumps(data, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        return default


class Timer:
    """Context manager para medir tempo de execução."""
    
    def __init__(self, name: str = "Operação"):
        self.name = name
        self.start_time: Optional[float] = None
        self.elapsed: Optional[float] = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        self.elapsed = time.time() - self.start_time
    
    def __str__(self):
        if self.elapsed is not None:
            return f"{self.name}: {format_duration(self.elapsed)}"
        return f"{self.name}: em andamento"
