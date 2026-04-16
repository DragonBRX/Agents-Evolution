#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    SANDBOX MODULAR PARA AGENTES INTELIGENTES - SISTEMA DE AUTONOMIA REAL
    Ambiente isolado, robusto e expansivel com suporte a 8 mentes profissionais.
    Integra ferramentas de Memoria Evolutiva, Auto-Reflexao e Aprendizado Recurvado.
    Otimizado para HD de 400GB em /media/dragonscp/Novo volume/modelo BRX.
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
import glob
from typing import Dict, Any, List, Callable, Optional, Union, Tuple
from datetime import datetime
from pathlib import Path

# ====================================================================================
# SECAO 1: CONFIGURACAO DE LOGGING PROFISSIONAL E TELEMETRIA
# ====================================================================================

class SandboxLogger:
    """Gerenciador de logs para o ambiente sandbox com suporte a cores e arquivos."""
    
    def __init__(self, name: str = "Sandbox", log_file: Optional[Path] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Formato detalhado para auditoria de autonomia
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(name)s] [%(threadName)s] %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para Console (Saida Padrao)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            
            # Handler para Arquivo (Persistencia no HD de 400GB)
            if log_file:
                try:
                    log_file.parent.mkdir(parents=True, exist_ok=True)
                    file_handler = logging.FileHandler(log_file, encoding='utf-8')
                    file_handler.setFormatter(formatter)
                    self.logger.addHandler(file_handler)
                except Exception as e:
                    print(f"ERRO: Falha ao criar arquivo de log no HD ({e}).")

    def info(self, msg: str): self.logger.info(msg)
    def error(self, msg: str): self.logger.error(msg)
    def warning(self, msg: str): self.logger.warning(msg)
    def debug(self, msg: str): self.logger.debug(msg)

# ====================================================================================
# SECAO 2: SISTEMA DE FERRAMENTAS (TOOL SYSTEM) COM AUTONOMIA
# ====================================================================================

class Tool:
    """Representa uma ferramenta registrada no sistema com suporte a telemetria."""
    
    def __init__(self, name: str, func: Callable, description: str, category: str = "geral"):
        self.name = name
        self.func = func
        self.description = description
        self.category = category
        self.usage_count = 0
        self.last_used: Optional[datetime] = None
        self.execution_history: List[Dict[str, Any]] = []

    def execute(self, *args, **kwargs) -> Any:
        """Executa a ferramenta com telemetria, tratamento de erros e logs de autonomia."""
        self.usage_count += 1
        self.last_used = datetime.now()
        start_time = time.time()
        
        try:
            result = self.func(*args, **kwargs)
            duration = time.time() - start_time
            
            # Registra sucesso no historico (limite de 50 registros para economia de memoria)
            if len(self.execution_history) > 50: self.execution_history.pop(0)
            self.execution_history.append({
                "timestamp": self.last_used.isoformat(),
                "duration": duration,
                "success": True
            })
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            error_trace = traceback.format_exc()
            
            self.execution_history.append({
                "timestamp": self.last_used.isoformat(),
                "duration": duration,
                "success": False,
                "error": str(e)
            })
            
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
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "avg_duration": sum(h['duration'] for h in self.execution_history) / max(1, len(self.execution_history))
        }

# ====================================================================================
# SECAO 3: CLASSE PRINCIPAL SANDBOX - EXPANSAO CUMULATIVA
# ====================================================================================

class Sandbox:
    """
    Ambiente de execucao seguro, robusto e AUTONOMO para agentes BRX.
    Combina a logica original de 8 mentes com ferramentas de Evolucao e Aprendizado.
    """
    
    def __init__(self, name: str = "BRX_Autonomous_Sandbox", storage_path: str = "/media/dragonscp/Novo volume/modelo BRX"):
        self.name = name
        # Protecao para caminhos com espacos usando Path do pathlib
        self.storage_root = Path(storage_path).absolute()
        self.tools: Dict[str, Tool] = {}
        
        # Inicializa diretorios e logs (Garantindo persistencia no HD de 400GB)
        self._ensure_directories()
        log_path = self.storage_root / "logs" / f"sandbox_autonomia_{int(time.time())}.log"
        self.logger = SandboxLogger(name, log_file=log_path)
        
        # Ambiente de execucao isolado (Dicionarios para exec())
        self.globals_env = {"__builtins__": __builtins__}
        self.locals_env = {}
        
        # Inicializacao do sistema
        self._setup_base_env()
        self._register_core_tools()
        self._register_autonomy_tools()
        
        self.logger.info(f"Sandbox Autonomo '{name}' inicializado com sucesso.")
        self.logger.info(f"Ponto de montagem de dados: {self.storage_root}")

    def _ensure_directories(self):
        """Cria a estrutura de pastas necessaria para o aprendizado recurvado no HD."""
        subdirs = [
            "dados", "logs", "parametros", "memorias", "exports", 
            "conhecimento_base", "licoes_aprendidas", "evolucao_logica"
        ]
        try:
            # Verifica se o caminho base existe ou pode ser criado
            if not self.storage_root.exists():
                self.storage_root.mkdir(parents=True, exist_ok=True)
            
            for sd in subdirs:
                (self.storage_root / sd).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            # Fallback para diretorio local se o HD nao estiver disponivel (Protecao de execucao)
            print(f"AVISO: Falha ao acessar HD ({e}). Usando diretorio local temporario.")
            self.storage_root = Path("./brx_local_storage").absolute()
            for sd in subdirs:
                (self.storage_root / sd).mkdir(parents=True, exist_ok=True)

    def _setup_base_env(self):
        """Configura as variaveis, bibliotecas e funcoes basicas do ambiente Python isolado."""
        self.locals_env.update({
            "print": self._agent_print,
            "datetime": datetime,
            "json": json,
            "time": time,
            "random": random,
            "re": re,
            "Path": Path,
            "glob": glob.glob,
            "STORAGE_PATH": str(self.storage_root),
            "AUTONOMY_LEVEL": "HIGH",
            "MIND_COUNT": 8
        })

    def _agent_print(self, *args, **kwargs):
        """Print customizado que redireciona para o logger do sistema com timestamp."""
        msg = " ".join(map(str, args))
        self.logger.info(f"[AUTONOMY_MIND] {msg}")

    # --- Registro de Ferramentas de Autonomia ---

    def register_tool(self, name: str, func: Callable, description: str, category: str = "custom"):
        """Adiciona uma nova ferramenta ao arsenal do agente de forma dinamica."""
        tool = Tool(name, func, description, category)
        self.tools[name] = tool
        self.locals_env[name] = tool.execute
        self.logger.info(f"Ferramenta registrada: '{name}' [{category}]")

    def _register_core_tools(self):
        """Registra o conjunto de ferramentas essenciais de manipulacao de dados."""
        
        def write_brx_data(filename: str, content: Union[str, Dict], subdir: str = "dados"):
            path = self.storage_root / subdir / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, (dict, list)):
                content = json.dumps(content, indent=4, ensure_ascii=False)
            path.write_text(str(content), encoding='utf-8')
            return f"Sucesso: Dados persistidos em {path}"

        def read_brx_data(filename: str, subdir: str = "dados"):
            path = self.storage_root / subdir / filename
            if not path.exists(): return {"error": f"Arquivo {filename} nao encontrado em {subdir}"}
            return path.read_text(encoding='utf-8')

        def run_shell_cmd(cmd: str):
            """Executa comandos no terminal Ubuntu de forma segura."""
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                return {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "exit_code": result.returncode
                }
            except Exception as e:
                return {"error": str(e)}

        self.register_tool("escrever_arquivo", write_brx_data, "Persiste dados ou JSON no HD de 400GB.", "arquivos")
        self.register_tool("ler_arquivo", read_brx_data, "Le arquivos do armazenamento BRX.", "arquivos")
        self.register_tool("executar_shell", run_shell_cmd, "Executa comandos no terminal Ubuntu Headless.", "sistema")

    def _register_autonomy_tools(self):
        """Registra ferramentas que permitem aos agentes evoluirem sozinhos (Aprendizado Recurvado)."""
        
        # 1. Memoria Evolutiva: Capacidade de buscar o que ja foi aprendido
        def buscar_conhecimento_antigo(pattern: str = "*.json", subdir: str = "parametros"):
            """Busca parametros gerados anteriormente para analise e evolucao."""
            search_path = str(self.storage_root / subdir / pattern)
            files = glob.glob(search_path)
            results = []
            for f in files[:10]: # Limite de 10 arquivos para processamento eficiente
                try:
                    results.append(json.loads(Path(f).read_text(encoding='utf-8')))
                except: continue
            return results

        # 2. Auto-Reflexao: Ferramenta para o agente avaliar sua propria logica
        def auto_refletir(pensamento: str, criterio: str = "qualidade"):
            """Permite ao agente avaliar o proprio raciocinio antes de finalizar o parametro."""
            words = pensamento.split()
            score = len(set(words)) / max(1, len(words)) # Diversidade lexical
            return {
                "raciocinio_analisado": pensamento,
                "score_autonomo": score,
                "aprovado": score > 0.6,
                "timestamp": datetime.now().isoformat()
            }

        # 3. Registro de Licoes: Persistencia de aprendizado real
        def registrar_licao(licao: str, contexto: str):
            """Salva uma licao aprendida pelo agente para uso em ciclos futuros."""
            filename = f"licao_{int(time.time())}_{random.randint(100, 999)}.json"
            data = {
                "contexto": contexto,
                "licao": licao,
                "timestamp": datetime.now().isoformat()
            }
            return write_brx_data(filename, data, subdir="licoes_aprendidas")

        self.register_tool("buscar_conhecimento", buscar_conhecimento_antigo, "Busca aprendizados passados no HD.", "autonomia")
        self.register_tool("auto_refletir", auto_refletir, "Avalia a qualidade do proprio raciocinio.", "autonomia")
        self.register_tool("registrar_licao", registrar_licao, "Persiste licoes aprendidas para evolucao futura.", "autonomia")

    # --- Execucao de Codigo ---

    def execute(self, code: str, context_name: str = "main_evolution") -> Dict[str, Any]:
        """Executa um bloco de codigo Python de forma isolada, capturando toda a saida e erros."""
        self.logger.info(f"Iniciando Ciclo de Evolucao: {context_name}")
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        start_time = time.time()
        result = {
            "success": False,
            "output": "",
            "error": None,
            "duration": 0,
            "context": context_name,
            "tools_used": []
        }

        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                # Execucao com isolamento de escopo
                exec(code, self.globals_env, self.locals_env)
            
            result["success"] = True
            result["output"] = stdout_capture.getvalue()
            
        except Exception:
            error_msg = traceback.format_exc()
            result["error"] = error_msg
            self.logger.error(f"FALHA NO CICLO '{context_name}':\n{error_msg}")
        
        finally:
            result["duration"] = time.time() - start_time
            # Coleta telemetria das ferramentas usadas neste ciclo
            result["tools_used"] = [t.to_dict() for t in self.tools.values() if t.usage_count > 0]
            self.logger.info(f"Ciclo '{context_name}' finalizado em {result['duration']:.4f}s")
            
        return result

    def get_system_report(self) -> Dict[str, Any]:
        """Gera um relatorio completo da saude e aprendizado do sistema Sandbox."""
        return {
            "sandbox_name": self.name,
            "storage_status": "ONLINE" if self.storage_root.exists() else "OFFLINE",
            "storage_path": str(self.storage_root),
            "tools_count": len(self.tools),
            "total_mind_threads": 8,
            "active_tools": [name for name, t in self.tools.items() if t.usage_count > 0]
        }
