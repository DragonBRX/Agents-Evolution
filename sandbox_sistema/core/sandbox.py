#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    SANDBOX MODULAR PARA AGENTES INTELIGENTES (v5.3)
    Ambiente isolado, robusto e expansível com suporte a 8 mentes profissionais.
    Mantém a base original e integra ferramentas avançadas do AgentForge.
"""

import sys
import json
import logging
import traceback
import io
import contextlib
import subprocess
import re
import time
import hashlib
import random
import threading
from typing import Dict, Any, List, Callable, Optional, Union, Tuple
from datetime import datetime
from pathlib import Path

# ====================================================================================
# SEÇÃO 1: CONFIGURAÇÃO DE LOGGING PROFISSIONAL
# ====================================================================================

class SandboxLogger:
    """Gerenciador de logs para o ambiente sandbox com suporte a cores e arquivos."""
    
    def __init__(self, name: str = "Sandbox", log_file: Optional[Path] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Formato detalhado
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s', 
            datefmt='%H:%M:%S'
        )
        
        # Handler para Console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            
            # Handler para Arquivo (se fornecido)
            if log_file:
                log_file.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def info(self, msg: str): self.logger.info(msg)
    def error(self, msg: str): self.logger.error(msg)
    def warning(self, msg: str): self.logger.warning(msg)
    def debug(self, msg: str): self.logger.debug(msg)

# ====================================================================================
# SEÇÃO 2: SISTEMA DE FERRAMENTAS (TOOL SYSTEM)
# ====================================================================================

class Tool:
    """Representa uma ferramenta registrada no sistema."""
    
    def __init__(self, name: str, func: Callable, description: str, category: str = "geral"):
        self.name = name
        self.func = func
        self.description = description
        self.category = category
        self.usage_count = 0
        self.last_used: Optional[datetime] = None

    def execute(self, *args, **kwargs) -> Any:
        """Executa a ferramenta com telemetria e tratamento de erros."""
        self.usage_count += 1
        self.last_used = datetime.now()
        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            error_trace = traceback.format_exc()
            return {
                "success": False,
                "error": str(e),
                "traceback": error_trace,
                "tool": self.name
            }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "usage_count": self.usage_count,
            "last_used": self.last_used.isoformat() if self.last_used else None
        }

# ====================================================================================
# SEÇÃO 3: CLASSE PRINCIPAL SANDBOX
# ====================================================================================

class Sandbox:
    """
    Ambiente de execução seguro e modular para agentes BRX.
    Combina a lógica original de 8 mentes com ferramentas avançadas.
    """
    
    def __init__(self, name: str = "BRX_Sandbox", storage_path: str = "/media/dragonscp/Novo volume/modelo BRX"):
        self.name = name
        self.storage_root = Path(storage_path)
        self.tools: Dict[str, Tool] = {}
        
        # Inicializa diretórios e logs
        self._ensure_directories()
        self.logger = SandboxLogger(name, log_file=self.storage_root / "logs" / f"sandbox_{int(time.time())}.log")
        
        # Ambiente de execução (Isolamento de variáveis)
        self.globals_env = {"__builtins__": __builtins__}
        self.locals_env = {}
        
        # Inicialização do sistema
        self._setup_base_env()
        self._register_core_tools()
        self.logger.info(f"Sandbox '{name}' inicializado com sucesso.")

    def _ensure_directories(self):
        """Cria a estrutura de pastas necessária no HD de 400GB."""
        subdirs = ["dados", "logs", "parametros", "memorias", "exports"]
        try:
            for sd in subdirs:
                (self.storage_root / sd).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            # Fallback para diretório local se o HD não estiver montado
            print(f"AVISO: Falha ao acessar HD ({e}). Usando diretório local.")
            self.storage_root = Path("./brx_local_storage")
            for sd in subdirs:
                (self.storage_root / sd).mkdir(parents=True, exist_ok=True)

    def _setup_base_env(self):
        """Configura as variáveis e funções básicas do ambiente Python."""
        self.locals_env.update({
            "print": self._agent_print,
            "datetime": datetime,
            "json": json,
            "time": time,
            "random": random,
            "re": re,
            "Path": Path,
            "STORAGE_PATH": self.storage_root,
            "VERSION": "5.3.0"
        })

    def _agent_print(self, *args, **kwargs):
        """Print customizado que redireciona para o logger do sistema."""
        msg = " ".join(map(str, args))
        self.logger.info(f"[AGENT_OUTPUT] {msg}")

    # --- Registro de Ferramentas ---

    def register_tool(self, name: str, func: Callable, description: str, category: str = "custom"):
        """Adiciona uma nova ferramenta ao arsenal do agente."""
        tool = Tool(name, func, description, category)
        self.tools[name] = tool
        self.locals_env[name] = tool.execute
        self.logger.info(f"Ferramenta '{name}' [{category}] registrada.")

    def _register_core_tools(self):
        """Registra o conjunto de ferramentas essenciais (Base + AgentForge)."""
        
        # 1. Ferramentas de Arquivo (Persistência no HD)
        def write_brx_data(filename: str, content: Union[str, Dict], subdir: str = "dados"):
            path = self.storage_root / subdir / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, (dict, list)):
                content = json.dumps(content, indent=4, ensure_ascii=False)
            path.write_text(str(content), encoding='utf-8')
            return f"Arquivo salvo em: {path}"

        def read_brx_data(filename: str, subdir: str = "dados"):
            path = self.storage_root / subdir / filename
            if not path.exists(): return {"error": "Arquivo não encontrado"}
            return path.read_text(encoding='utf-8')

        # 2. Ferramentas de Sistema (Inspiradas no AgentForge)
        def run_shell_cmd(cmd: str):
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                return {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "exit_code": result.returncode
                }
            except Exception as e:
                return {"error": str(e)}

        # 3. Ferramentas de Análise de Qualidade (Para Parâmetros)
        def analyze_param_quality(text: str):
            words = text.split()
            unique_words = set(w.lower() for w in words)
            return {
                "length": len(text),
                "word_count": len(words),
                "vocabulary_richness": len(unique_words) / max(1, len(words)),
                "timestamp": datetime.now().isoformat()
            }

        # Registro das ferramentas core
        self.register_tool("escrever_arquivo", write_brx_data, "Salva dados ou JSON no HD de 400GB.", "arquivos")
        self.register_tool("ler_arquivo", read_brx_data, "Lê arquivos do armazenamento BRX.", "arquivos")
        self.register_tool("executar_shell", run_shell_cmd, "Executa comandos no terminal Ubuntu (Headless).", "sistema")
        self.register_tool("analisar_qualidade", analyze_param_quality, "Avalia métricas de qualidade do parâmetro gerado.", "analise")

    # --- Execução de Código ---

    def execute(self, code: str, context_name: str = "main") -> Dict[str, Any]:
        """Executa um bloco de código Python de forma isolada e segura."""
        self.logger.info(f"Iniciando execução do contexto: {context_name}")
        
        # Captura de saída
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        start_time = time.time()
        result = {
            "success": False,
            "output": "",
            "error": None,
            "duration": 0,
            "context": context_name
        }

        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                # O coração da execução: exec() com escopos controlados
                exec(code, self.globals_env, self.locals_env)
            
            result["success"] = True
            result["output"] = stdout_capture.getvalue()
            
        except Exception:
            error_msg = traceback.format_exc()
            result["error"] = error_msg
            self.logger.error(f"Erro na execução do contexto '{context_name}':\n{error_msg}")
        
        finally:
            result["duration"] = time.time() - start_time
            self.logger.info(f"Contexto '{context_name}' finalizado em {result['duration']:.4f}s")
            
        return result

    def get_status(self) -> Dict[str, Any]:
        """Retorna o estado atual do Sandbox."""
        return {
            "name": self.name,
            "storage": str(self.storage_root),
            "tools_registered": list(self.tools.keys()),
            "active_variables": [k for k in self.locals_env.keys() if not k.startswith('_')],
            "uptime_seconds": time.time() - psutil.boot_time() if 'psutil' in sys.modules else "N/A"
        }
EOF
