#!/bin/bash

# ==============================================================================
# SETUP ULTRA-RÁPIDO - AGENTS EVOLUTION BRX
# Focado em: Performance, HD de 400GB e dependências mínimas.
# ==============================================================================

set -e

echo "🚀 INICIANDO SETUP RÁPIDO..."

# 1. Configuração do HD (Cria apenas o que falta)
STORAGE_ROOT="/media/dragonscp/Novo volume/modelo BRX"
PROJECT_DIR="$HOME/Agents-Evolution-Sandbox"

echo "💾 Verificando HD: $STORAGE_ROOT"
mkdir -p "$STORAGE_ROOT/dados" "$STORAGE_ROOT/logs" "$STORAGE_ROOT/parametros" "$STORAGE_ROOT/memorias" "$STORAGE_ROOT/licoes_aprendidas"

# 2. Ambiente Python (Sem apt update pesado)
echo "🐍 Configurando ambiente virtual..."
mkdir -p "$PROJECT_DIR/core"
cd "$PROJECT_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# 3. Instalação de bibliotecas (Apenas o essencial, sem cache para ser mais rápido)
echo "📚 Instalando bibliotecas essenciais..."
pip install --no-cache-dir requests beautifulsoup4 colorama sqlalchemy pandas numpy flask

# 4. Download dos arquivos do GitHub (Garantindo que você tenha a versão mais nova)
echo "📥 Baixando scripts de autonomia..."
curl -s -o core/sandbox.py https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/sandbox_sistema/core/sandbox.py
curl -s -o gerador_parametros.py https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/gerador_parametros.py

echo ""
echo "✅ TUDO PRONTO EM TEMPO RECORDE!"
echo "=============================================================================="
echo "Para rodar a geração autônoma agora:"
echo "source venv/bin/activate && python3 gerador_parametros.py"
echo "=============================================================================="
