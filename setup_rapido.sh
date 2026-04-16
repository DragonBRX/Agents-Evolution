#!/bin/bash

# ==============================================================================
# SETUP ULTRA-RAPIDO - AGENTS EVOLUTION BRX
# Focado em: Performance, HD de 400GB e dependencias minimas.
# Estilo Profissional: Sem emojis e com execucao automatica.
# ==============================================================================

set -e

echo "INICIANDO SETUP RAPIDO..."

# 1. Configuracao do HD (Cria apenas o que falta)
STORAGE_ROOT="/media/dragonscp/Novo volume/modelo BRX"
PROJECT_DIR="$HOME/Agents-Evolution-Sandbox"

echo "Verificando ponto de montagem: $STORAGE_ROOT"

# Tenta criar os diretorios. Se falhar por permissao, avisa o usuario.
if [ -d "$STORAGE_ROOT" ] || mkdir -p "$STORAGE_ROOT" 2>/dev/null; then
    echo "HD detectado. Criando estrutura de pastas..."
    mkdir -p "$STORAGE_ROOT/dados" "$STORAGE_ROOT/logs" "$STORAGE_ROOT/parametros" "$STORAGE_ROOT/memorias" "$STORAGE_ROOT/licoes_aprendidas"
else
    echo "AVISO: Nao foi possivel acessar o HD em $STORAGE_ROOT."
    echo "O sistema usara uma pasta local temporaria para nao travar a instalacao."
fi

# 2. Ambiente Python
echo "Configurando ambiente virtual..."
mkdir -p "$PROJECT_DIR/sandbox_sistema/core"
cd "$PROJECT_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Ativa o ambiente virtual
source venv/bin/activate

# 3. Instalacao de bibliotecas (Apenas o essencial)
echo "Instalando bibliotecas de producao..."
pip install --no-cache-dir requests beautifulsoup4 colorama sqlalchemy pandas numpy flask

# 4. Download dos arquivos do GitHub (Garantindo a versao limpa)
echo "Sincronizando scripts de autonomia..."
curl -s -o sandbox_sistema/__init__.py https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/sandbox_sistema/__init__.py
curl -s -o sandbox_sistema/core/__init__.py https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/sandbox_sistema/core/__init__.py
curl -s -o sandbox_sistema/core/sandbox.py https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/sandbox_sistema/core/sandbox.py
curl -s -o gerador_parametros.py https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/gerador_parametros.py

# 5. Criacao do script de execucao direta (run.sh)
echo "Criando atalho de execucao..."
cat << 'EOF' > run.sh
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 gerador_parametros.py
EOF
chmod +x run.sh

echo ""
echo "=============================================================================="
echo "SETUP CONCLUIDO!"
echo "INICIANDO MOTOR DE PRODUCAO REAL AGORA..."
echo "=============================================================================="

# 6. Execucao Automatica
./run.sh
