#!/bin/bash

# ==============================================================================
# SETUP ULTRA-RAPIDO - AGENTS EVOLUTION BRX
# Focado em: Performance, HD de 400GB e dependencias minimas.
# Sem emojis e com execucao automatica.
# ==============================================================================

set -e

echo "INICIANDO SETUP RAPIDO..."

# 1. Configuracao do HD (Cria apenas o que falta)
STORAGE_ROOT="/media/dragonscp/Novo volume/modelo BRX"
PROJECT_DIR="$HOME/Agents-Evolution-Sandbox"

echo "Verificando HD: $STORAGE_ROOT"
mkdir -p "$STORAGE_ROOT/dados" "$STORAGE_ROOT/logs" "$STORAGE_ROOT/parametros" "$STORAGE_ROOT/memorias" "$STORAGE_ROOT/licoes_aprendidas"

# 2. Ambiente Python (Sem apt update pesado)
echo "Configurando ambiente virtual..."
mkdir -p "$PROJECT_DIR/core"
cd "$PROJECT_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Ativa o ambiente virtual para instalar as dependencias
source venv/bin/activate

# 3. Instalacao de bibliotecas (Apenas o essencial, sem cache para ser mais rapido)
echo "Instalando bibliotecas essenciais..."
pip install --no-cache-dir requests beautifulsoup4 colorama sqlalchemy pandas numpy flask

# 4. Download dos arquivos do GitHub (Garantindo que voce tenha a versao mais nova)
echo "Baixando scripts de autonomia..."
curl -s -o core/sandbox.py https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/sandbox_sistema/core/sandbox.py
curl -s -o gerador_parametros.py https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/gerador_parametros.py

# 5. Criacao de um script de execucao direta (run.sh)
echo "Criando script de execucao direta..."
cat << 'EOF' > run.sh
#!/bin/bash
source venv/bin/activate
python3 gerador_parametros.py
EOF
chmod +x run.sh

echo ""
echo "=============================================================================="
echo "SETUP CONCLUIDO EM TEMPO RECORDE!"
echo "INICIANDO GERACAO AUTONOMA AGORA..."
echo "=============================================================================="

# 6. Execucao Automatica
./run.sh
