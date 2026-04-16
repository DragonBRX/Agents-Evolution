#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    SANDBOX MODULAR PARA AGENTES INTELIGENTES (v5.2)
    Ambiente isolado com ferramentas avançadas e suporte a raciocínio multi-agente.
"""

import sys
import json
import logging
import traceback
import io
import contextlib
import subprocess
import re
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from pathlib import Path

# ====================================================================================
# CONFIGURAÇÃO DE LOGGING
# ====================================================================================

class SandboxLogger:
    """Logger customizado para o ambiente sandbox."""
    
    def __init__(self, name: str = "Sandbox"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%H:%M:%S')
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

    def info(self, msg: str): self.logger.info(msg)
    def error(self, msg: str): self.logger.error(msg)
    def warning(self, msg: str): self.logger.warning(msg)

# ====================================================================================
# SISTEMA DE FERRAMENTAS (TOOLS)
# ====================================================================================

class Tool:
    """Representa uma ferramenta que o agente pode utilizar."""
    
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description
        self.usage_count = 0

    def execute(self, *args, **kwargs) -> Any:
        """Executa a função da ferramenta com tratamento de erros."""
        self.usage_count += 1
        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            return f"Erro ao executar ferramenta '{self.name}': {str(e)}"

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "description": self.description,
            "usage_count": self.usage_count
        }

# ====================================================================================
# CLASSE PRINCIPAL: SANDBOX
# ====================================================================================

class Sandbox:
    """
    Ambiente isolado para execução de agentes.
    Integra ferramentas de Shell, Python, Arquivos e Lógicas de Raciocínio.
    """
    
    def __init__(self, name: str = "DefaultSandbox", storage_path: str = "/media/dragonscp/Novo volume/modelo BRX"):
        self.name = name
        self.storage_path = Path(storage_path)
        self.tools: Dict[str, Tool] = {}
        self.logger = SandboxLogger(name)
        self.globals_env = {"__builtins__": __builtins__}
        self.locals_env = {}
        self._setup_initial_env()
        self._ensure_storage()
        self._register_default_tools()

    def _ensure_storage(self):
        """Garante que o diretório de armazenamento existe."""
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Armazenamento configurado em: {self.storage_path}")
        except Exception as e:
            self.logger.warning(f"Erro no HD: {e}. Usando './data_sandbox'")
            self.storage_path = Path("./data_sandbox")
            self.storage_path.mkdir(parents=True, exist_ok=True)

    def _setup_initial_env(self):
        """Configura o ambiente inicial."""
        self.locals_env["print"] = self._custom_print
        self.locals_env["datetime"] = datetime
        self.locals_env["json"] = json
        self.locals_env["storage_path"] = str(self.storage_path)

    def _custom_print(self, *args, **kwargs):
        message = " ".join(map(str, args))
        self.logger.info(f"[AGENT] {message}")

    def register_tool(self, name: str, func: Callable, description: str):
        tool = Tool(name, func, description)
        self.tools[name] = tool
        self.locals_env[name] = tool.execute
        self.logger.info(f"Ferramenta registrada: '{name}'")

    def _register_default_tools(self):
        """Registra as ferramentas base inspiradas no AgentForge."""
        
        # 1. Ferramenta de Shell (Segura)
        def execute_shell(command: str):
            """Executa comandos shell no sistema."""
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
                return {"stdout": result.stdout, "stderr": result.stderr, "code": result.returncode}
            except Exception as e:
                return {"error": str(e)}
        
        # 2. Ferramenta de Arquivos
        def read_file(path: str):
            """Lê conteúdo de um arquivo."""
            full_path = self.storage_path / path
            if not full_path.exists(): return f"Erro: Arquivo {path} não encontrado."
            return full_path.read_text(encoding='utf-8')

        def write_file(path: str, content: str):
            """Escreve conteúdo em um arquivo no HD."""
            full_path = self.storage_path / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
            return f"Sucesso: {path} salvo."

        # 3. Analisador de Texto (Métricas de Qualidade)
        def analyze_text(text: str):
            """Analisa métricas do texto para qualidade de parâmetros."""
            words = text.split()
            return {
                "word_count": len(words),
                "char_count": len(text),
                "unique_words": len(set(w.lower() for w in words)),
                "complexity": len(set(words)) / max(1, len(words))
            }

        self.register_tool("shell", execute_shell, "Executa comandos no terminal Ubuntu.")
        self.register_tool("ler_arquivo", read_file, "Lê arquivos do armazenamento BRX.")
        self.register_tool("escrever_arquivo", write_file, "Salva dados no armazenamento BRX.")
        self.register_tool("analisar_texto", analyze_text, "Avalia a qualidade e métricas do texto.")

    def run_code(self, code: str) -> Dict[str, Any]:
        """Executa código Python no sandbox."""
        self.logger.info(f"Executando raciocínio no sandbox '{self.name}'...")
        stdout, stderr = io.StringIO(), io.StringIO()
        result = {"success": False, "output": "", "error": None, "time": None}
        start = datetime.now()
        
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(code, self.globals_env, self.locals_env)
            result["success"] = True
            result["output"] = stdout.getvalue()
        except Exception:
            result["error"] = traceback.format_exc()
            self.logger.error(f"Falha na execução:\n{result['error']}")
        finally:
            result["time"] = str(datetime.now() - start)
            
        return result
