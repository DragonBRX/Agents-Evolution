#!/bin/bash

# ==============================================================================
# SCRIPT MESTRE DE CONFIGURAÇÃO - AGENTS EVOLUTION BRX (UBUNTU)
# Este script faz o setup completo: HD, dependências e ambiente de execução.
# ==============================================================================

set -e # Para em caso de erro

echo "INICIANDO SETUP COMPLETO DO AGENTS-EVOLUTION NO UBUNTU..."

# 1. Definir caminhos de armazenamento no HD de 400GB
STORAGE_ROOT="/media/dragonscp/Novo volume/modelo BRX"
PROJECT_DIR="$HOME/Agents-Evolution-Sandbox"

echo "Configurando diretorios no HD: $STORAGE_ROOT"
sudo mkdir -p "$STORAGE_ROOT/dados" "$STORAGE_ROOT/logs" "$STORAGE_ROOT/parametros"
sudo chown -R $USER:$USER "$STORAGE_ROOT"

# 2. Atualizar sistema e instalar pacotes base
echo "Instalando dependencias do sistema (Python, Git, SQLite)..."
sudo apt update -y && sudo apt install -y python3 python3-pip python3-venv git libsqlite3-dev

# 3. Criar pasta do projeto e ambiente virtual
echo "Criando pasta do projeto em $PROJECT_DIR..."
mkdir -p "$PROJECT_DIR/core"
cd "$PROJECT_DIR"

echo "Configurando ambiente virtual Python..."
python3 -m venv venv
source venv/bin/activate

# 4. Instalar bibliotecas Python necessarias
echo "Instalando bibliotecas (Requests, BS4, Flask, Matplotlib, Pandas)..."
pip install --upgrade pip
pip install requests beautifulsoup4 colorama flask matplotlib numpy pandas sqlalchemy

# 5. Criar o arquivo core/sandbox.py com o caminho do HD ja fixado
echo "Gerando codigo do Sandbox..."
cat << 'EOF' > core/sandbox.py
import sys, json, logging, traceback, io, contextlib
from typing import Dict, Any, List, Callable
from datetime import datetime
from pathlib import Path

class Sandbox:
    def __init__(self, name="BRX_Sandbox", storage="/media/dragonscp/Novo volume/modelo BRX"):
        self.name = name
        self.storage = Path(storage)
        self.tools = {}
        self.globals_env = {"__builtins__": __builtins__}
        self.locals_env = {"print": self._print, "datetime": datetime, "json": json}
        self._ensure_storage()

    def _ensure_storage(self):
        self.storage.mkdir(parents=True, exist_ok=True)
        print(f"DEBUG: Armazenamento em {self.storage}")

    def _print(self, *args):
        print(f"[{self.name}] {' '.join(map(str, args))}")

    def register_tool(self, name, func):
        self.tools[name] = func
        self.locals_env[name] = func

    def run(self, code):
        try:
            exec(code, self.globals_env, self.locals_env)
            return True
        except Exception:
            print(traceback.format_exc()); return False
EOF

# 6. Criar o script de execucao inicial (gerador_brx.py)
echo "Criando script de geracao de parametros..."
cat << 'EOF' > gerador_brx.py
from core.sandbox import Sandbox
import time

def main():
    sb = Sandbox("Gerador_BRX")
    
    # Ferramenta de exemplo: Log de Parametro
    def salvar_parametro(tipo, conteudo):
        path = "/media/dragonscp/Novo volume/modelo BRX/parametros/params.txt"
        with open(path, "a") as f:
            f.write(f"[{time.ctime()}] {tipo}: {conteudo}\n")
        return "Salvo no HD"

    sb.register_tool("salvar", salvar_parametro)

    codigo = """
print("Iniciando Evolucao de Parametros BRX...")
status = salvar("POSITIVO", "Nova logica de inteligencia coletiva detectada.")
print(f"Status do HD: {status}")
"""
    sb.run(codigo)

if __name__ == "__main__":
    main()
EOF

echo ""
echo "=============================================================================="
echo "SETUP CONCLUIDO! O AMBIENTE ESTA PRONTO NO SEU HD."
echo "=============================================================================="
echo "Para rodar agora, cole estes dois comandos:"
echo "source venv/bin/activate"
echo "python3 gerador_brx.py"
echo "=============================================================================="
