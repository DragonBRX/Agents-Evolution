"""
Sistema de logging profissional com rotação de arquivos.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Formatter com cores para console."""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA + Style.BRIGHT
    }
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, '')
        reset = Style.RESET_ALL
        
        # Adiciona emoji baseado no nível
        emojis = {
            'DEBUG': '',
            'INFO': '',
            'WARNING': '',
            'ERROR': '',
            'CRITICAL': ''
        }
        
        record.levelname = f"{color}{emojis.get(record.levelname, '')} {record.levelname}{reset}"
        return super().format(record)


class AgentLogger:
    """Logger especializado para agentes."""
    
    def __init__(self, agente_nome: str):
        self.agente_nome = agente_nome
        self.logger = logging.getLogger(f"agente.{agente_nome}")
    
    def pensamento(self, mensagem: str):
        """Loga um pensamento do agente."""
        self.logger.debug(f" [{self.agente_nome}] {mensagem}")
    
    def acao(self, mensagem: str):
        """Loga uma ação do agente."""
        self.logger.info(f" [{self.agente_nome}] {mensagem}")
    
    def critica(self, mensagem: str):
        """Loga uma crítica do agente."""
        self.logger.info(f" [{self.agente_nome}] {mensagem}")
    
    def erro(self, mensagem: str):
        """Loga um erro do agente."""
        self.logger.error(f" [{self.agente_nome}] {mensagem}")


def setup_logging(
    nivel: str = "INFO",
    formato: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    arquivo: Optional[str] = None,
    max_bytes: int = 10485760,
    backup_count: int = 5,
    console: bool = True
) -> logging.Logger:
    """
    Configura o sistema de logging.
    
    Args:
        nivel: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        formato: Formato das mensagens de log
        arquivo: Caminho do arquivo de log (None para desabilitar)
        max_bytes: Tamanho máximo do arquivo antes da rotação
        backup_count: Número de arquivos de backup
        console: Se True, loga também no console
    
    Returns:
        Logger configurado
    """
    # Logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, nivel.upper()))
    
    # Remove handlers existentes
    root_logger.handlers = []
    
    # Formatter padrão
    formatter = logging.Formatter(formato, datefmt="%Y-%m-%d %H:%M:%S")
    
    # Handler de arquivo com rotação
    if arquivo:
        log_path = Path(arquivo)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            arquivo,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Handler de console com cores
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredFormatter(formato, datefmt="%H:%M:%S"))
        root_logger.addHandler(console_handler)
    
    return root_logger


def get_logger(nome: str) -> logging.Logger:
    """Obtém um logger com o nome especificado."""
    return logging.getLogger(nome)


def get_agent_logger(agente_nome: str) -> AgentLogger:
    """Obtém um logger especializado para um agente."""
    return AgentLogger(agente_nome)


# Logger do sistema
logger = get_logger("sistema")
