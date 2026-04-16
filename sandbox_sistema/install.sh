#!/bin/bash

# ==============================================================================
# SCRIPT DE INSTALAÇÃO AUTOMATIZADA - AMBIENTE SANDBOX AGENTS-EVOLUTION
# Alvo: Ubuntu 22.04+ (ou similares)
# ==============================================================================

echo "🚀 Iniciando instalação do ambiente de agentes no Ubuntu..."

# 1. Atualizar repositórios
echo "📦 Atualizando lista de pacotes..."
sudo apt update -y

# 2. Instalar dependências do sistema
echo "🛠️ Instalando dependências essenciais do sistema..."
sudo apt install -y python3 python3-pip python3-venv git curl build-essential libsqlite3-dev

# 3. Criar ambiente virtual Python (Recomendado)
echo "🐍 Criando ambiente virtual Python (venv)..."
python3 -m venv venv
source venv/bin/activate

# 4. Instalar dependências Python
echo "📚 Instalando bibliotecas Python necessárias..."
pip install --upgrade pip
pip install requests beautifulsoup4 colorama flask matplotlib numpy pandas sqlalchemy

# 5. Configurar diretórios de armazenamento no HD
STORAGE_PATH="/media/dragonscp/Novo volume/modelo BRX"
echo "💾 Configurando diretório de armazenamento no HD: $STORAGE_PATH"

if [ -d "/media/dragonscp" ]; then
    sudo mkdir -p "$STORAGE_PATH"
    sudo chown -R $USER:$USER "$STORAGE_PATH"
    echo "✅ Diretório criado e permissões ajustadas."
else
    echo "⚠️ HD não detectado em /media/dragonscp. O sistema usará armazenamento local por padrão."
fi

# 6. Finalização
echo ""
echo "=============================================================================="
echo "✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "=============================================================================="
echo "Para começar:"
echo "1. Ative o ambiente virtual: source venv/bin/activate"
echo "2. Execute o teste: python3 test_sandbox.py"
echo "3. Execute o exemplo avançado: python3 exemplo_avancado.py"
echo "=============================================================================="
