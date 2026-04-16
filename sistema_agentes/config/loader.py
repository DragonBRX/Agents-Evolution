"""
Loader de configuração YAML com suporte a variáveis de ambiente.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class ConfigLoader:
    """Carrega e gerencia configurações do sistema."""
    
    config_path: Path = Path(__file__).parent / "settings.yaml"
    _config: Dict[str, Any] = None
    
    def __post_init__(self):
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carrega configuração do arquivo YAML."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Substitui variáveis de ambiente
        config = self._substituir_env_vars(config)
        
        return config
    
    def _substituir_env_vars(self, obj: Any) -> Any:
        """Substitui variáveis de ambiente no formato ${VAR}."""
        if isinstance(obj, dict):
            return {k: self._substituir_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._substituir_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            import re
            pattern = r'\$\{([^}]+)\}'
            
            def replace_var(match):
                var_name = match.group(1)
                return os.getenv(var_name, match.group(0))
            
            return re.sub(pattern, replace_var, obj)
        return obj
    
    def get(self, *keys: str, default: Any = None) -> Any:
        """
        Obtém valor de configuração por chaves aninhadas.
        
        Ex: config.get('sistema', 'execucao', 'max_workers')
        """
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def get_agente(self, agente_id: int) -> Optional[Dict[str, Any]]:
        """Obtém configuração de um agente específico."""
        agentes = self.get('agentes', 'lista', default=[])
        for agente in agentes:
            if agente.get('id') == agente_id:
                return agente
        return None
    
    def get_all_agentes(self) -> list:
        """Retorna lista de todos os agentes configurados."""
        return self.get('agentes', 'lista', default=[])
    
    def get_topicos(self) -> list:
        """Retorna lista de tópicos padrão."""
        return self.get('topicos', 'padrao', default=[])
    
    @property
    def sistema_nome(self) -> str:
        return self.get('sistema', 'nome', default='Sistema Multi-Agente')
    
    @property
    def sistema_versao(self) -> str:
        return self.get('sistema', 'versao', default='1.0.0')
    
    @property
    def db_path(self) -> str:
        """Retorna caminho do banco de dados SQLite."""
        return self.get('banco_dados', 'sqlite', 'path', default='data/flash_sistema.db')
    
    @property
    def logging_config(self) -> Dict[str, Any]:
        """Retorna configuração de logging."""
        return self.get('sistema', 'logging', default={})


# Instância global de configuração
_config_instance: Optional[ConfigLoader] = None


def get_config() -> ConfigLoader:
    """Retorna instância singleton de configuração."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader()
    return _config_instance


def reload_config():
    """Recarrega configuração do arquivo."""
    global _config_instance
    _config_instance = ConfigLoader()
