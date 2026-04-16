#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    SANDBOX MODULAR PARA AGENTES INTELIGENTES
    Ambiente isolado para execução de ferramentas e código Python.
"""

import sys
import json
import logging
import traceback
import io
import contextlib
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
        
        # Formato limpo e profissional
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%H:%M:%S')
        
        # Console Handler
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
        """Retorna metadados da ferramenta."""
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
    Controla ferramentas disponíveis, executa código e gera logs.
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

    def _ensure_storage(self):
        """Garante que o diretório de armazenamento existe."""
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Armazenamento configurado em: {self.storage_path}")
        except Exception as e:
            self.logger.warning(f"Não foi possível criar diretório no HD: {e}. Usando diretório local.")
            self.storage_path = Path("./data_sandbox")
            self.storage_path.mkdir(parents=True, exist_ok=True)

    def _setup_initial_env(self):
        """Configura o ambiente inicial com funções básicas seguras."""
        # Podemos restringir o que o agente pode fazer aqui
        self.locals_env["print"] = self._custom_print
        self.locals_env["datetime"] = datetime

    def _custom_print(self, *args, **kwargs):
        """Redireciona o print para o logger do sandbox."""
        message = " ".join(map(str, args))
        self.logger.info(f"[AGENT PRINT] {message}")

    def register_tool(self, name: str, func: Callable, description: str):
        """Registra uma nova ferramenta no sandbox."""
        tool = Tool(name, func, description)
        self.tools[name] = tool
        # Disponibiliza a ferramenta no ambiente de execução
        self.locals_env[name] = tool.execute
        self.logger.info(f"Ferramenta registrada: '{name}' - {description}")

    def list_tools(self) -> List[Dict[str, str]]:
        """Lista todas as ferramentas registradas."""
        return [tool.to_dict() for tool in self.tools.values()]

    def run_code(self, code: str) -> Dict[str, Any]:
        """
        Executa código Python de forma isolada e captura a saída.
        """
        self.logger.info(f"Iniciando execução de código no sandbox '{self.name}'...")
        
        # Captura stdout e stderr
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        result = {
            "success": False,
            "output": "",
            "error": None,
            "execution_time": None
        }
        
        start_time = datetime.now()
        
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                # Executa o código usando exec no ambiente controlado
                exec(code, self.globals_env, self.locals_env)
            
            result["success"] = True
            result["output"] = stdout.getvalue()
            self.logger.info("Execução concluída com sucesso.")
            
        except Exception:
            error_msg = traceback.format_exc()
            result["error"] = error_msg
            self.logger.error(f"Erro durante a execução:\n{error_msg}")
        
        finally:
            end_time = datetime.now()
            result["execution_time"] = str(end_time - start_time)
            
        return result

    def execute_action(self, tool_name: str, **kwargs) -> Any:
        """
        Executa uma ação específica chamando uma ferramenta registrada.
        """
        if tool_name not in self.tools:
            msg = f"Ferramenta '{tool_name}' não encontrada no sandbox."
            self.logger.warning(msg)
            return msg
        
        self.logger.info(f"Agente chamando ferramenta: '{tool_name}' com parâmetros: {kwargs}")
        return self.tools[tool_name].execute(**kwargs)

# ====================================================================================
# EXEMPLO DE USO (Pode ser removido ou importado)
# ====================================================================================

if __name__ == "__main__":
    # Esta seção serve para testes rápidos se o arquivo for executado diretamente
    sb = Sandbox("TesteManual")
    
    def mock_search(query: str):
        return f"Resultados para '{query}': [Dado 1, Dado 2, Dado 3]"
    
    sb.register_tool("busca_web", mock_search, "Simula uma busca na internet.")
    
    test_code = """
print('Olá do Sandbox!')
resultado = busca_web(query='Inteligência Artificial')
print(f'Resultado da busca: {resultado}')
"""
    res = sb.run_code(test_code)
    print("\n--- RESULTADO FINAL ---")
    print(json.dumps(res, indent=2))
