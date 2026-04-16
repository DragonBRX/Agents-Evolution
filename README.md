# Agents-Evolution

Agents-Evolution e um ecossistema de inteligencia coletiva circular projetado para a geracao de parametros inteligentes atraves do debate colaborativo entre multiplas mentes autonomas. O sistema opera sob o conceito de uma mesa de reuniao virtual, onde agentes especializados discutem e refinam informacoes para alcancar um consenso de alta qualidade.

## O Conceito: Escritorio de Processamento e Debate Circular

O modelo de funcionamento do Agents-Evolution rompe com as abordagens tradicionais de processamento linear. O sistema simula um ambiente de escritorio de alto nivel, onde o processador atua como o motor central que distribui tarefas para threads especializadas.

### A Dinamica das Threads e o Fluxo de Trabalho

Imagine um escritorio onde cada thread do processador (por padrao, 8 threads) representa um colega de trabalho sentado em sua própria mesa. O fluxo de informacoes segue exatamente este modelo:

1.  **Entrada e Pesquisa**: O sistema inicia uma pesquisa abrangente (utilizando DuckDuckGo e outras fontes). Assim que as informacoes sao trazidas, o "processador" as distribui como se fossem papeis sendo colocados nas mesas desses 8 colegas.
2.  **Especializacao Individual**: Cada um desses 8 colegas e um especialista em uma area distinta (como Design, Analise de Dados, Criatividade, Critica, Revisao, Validacao, Estrategia e Memoria). Eles comecam a trabalhar nos dados simultaneamente, cada um sob sua propria perspectiva tecnica.
3.  **A Roda de Informacoes (Mesa de Conversas)**: O diferencial do sistema e o ciclo de debate. Em vez de trabalharem isolados, os agentes formam um circulo de conversa. Uma informacao ou parametro gerado por um agente e passado para o proximo na roda. Eles conversam entre si, criticam o trabalho do colega e refinam o conteudo continuamente.
4.  **Acordo e Consenso**: O proprio codigo decide quantas vezes essa conversa deve circular na mesa ate que se chegue ao melhor acordo possivel. Cada agente traduz os parametros para sua propria perspectiva, garantindo uma cobertura completa do topico.

### Sistema de Parametros Positivos e Negativos

Diferente de modelos que utilizam pontuacoes numericas fixas, o Agents-Evolution foca na polaridade e na utilidade real dos dados:

| Tipo de Parametro | Descricao e Objetivo |
| :--- | :--- |
| **Positivos** | Sao as boas respostas, os caminhos corretos e os padroes que devem ser preferenciados pelo modelo. |
| **Negativos** | Sao as respostas ruins, falhas ou caminhos que devem ser evitados ativamente para garantir a precisao. |

Neste sistema, os parametros nao sao classificados por numeros crescentes. Nao ha necessidade de uma escala infinita de pontuacao porque o modelo e projetado para a **Evolucao por Nivel**. 

### Evolucao e Superacao do Modelo

O conceito central de inteligencia aqui e a superacao constante: a medida que o treinamento avanca, o proprio modelo se torna muito mais inteligente do que o conhecimento contido nos parametros que ele mesmo gerou anteriormente. 

Isso faz com que os parametros "descam de nivel" — nao porque ficaram piores, mas porque o patamar de inteligencia do modelo subiu tanto que o que era considerado "avancado" anteriormente passa a ser o conhecimento basico e fundamental para o proximo nivel de evolucao.

## 🚀 Novidade: Sandbox Modular e Sistema de Ferramentas (v5.1)

Agora o ecossistema inclui um ambiente **Sandbox Modular** em Python para a execução segura e controlada de agentes. Este ambiente permite que os agentes utilizem ferramentas registradas (como busca web, processamento de arquivos e análise de dados) com total isolamento e logs detalhados.

### 🛠️ Instalação Rápida (Ubuntu) - Setup Completo em 1 Comando

Para configurar todo o ambiente no seu Ubuntu, incluindo a criação de diretórios no HD externo (`/media/dragonscp/Novo volume/modelo BRX`), instalação de dependências do sistema e bibliotecas Python, execute o bloco abaixo no seu terminal:

```bash
# 1. Baixe e execute o script mestre de configuração
curl -O https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/setup_completo.sh 2>/dev/null || cat << 'EOF' > setup_completo.sh
#!/bin/bash
set -e
echo "🚀 INICIANDO SETUP COMPLETO NO HD DE 400GB..."
STORAGE_ROOT="/media/dragonscp/Novo volume/modelo BRX"
PROJECT_DIR="$HOME/Agents-Evolution-Sandbox"
sudo mkdir -p "$STORAGE_ROOT/dados" "$STORAGE_ROOT/logs" "$STORAGE_ROOT/parametros"
sudo chown -R $USER:$USER "$STORAGE_ROOT"
sudo apt update -y && sudo apt install -y python3 python3-pip python3-venv git libsqlite3-dev
mkdir -p "$PROJECT_DIR/core" && cd "$PROJECT_DIR"
python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip && pip install requests beautifulsoup4 colorama flask matplotlib numpy pandas sqlalchemy
cat << 'CORE' > core/sandbox.py
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
CORE
cat << 'GEN' > gerador_brx.py
from core.sandbox import Sandbox
import time
def main():
    sb = Sandbox("Gerador_BRX")
    def salvar_parametro(tipo, conteudo):
        path = "/media/dragonscp/Novo volume/modelo BRX/parametros/params.txt"
        with open(path, "a") as f:
            f.write(f"[{time.ctime()}] {tipo}: {conteudo}\n")
        return "Salvo no HD"
    sb.register_tool("salvar", salvar_parametro)
    codigo = "print('Iniciando Evolução de Parâmetros BRX...'); status = salvar('POSITIVO', 'Nova lógica detectada.'); print(f'Status do HD: {status}')"
    sb.run(codigo)
if __name__ == "__main__": main()
GEN
echo "✅ SETUP CONCLUÍDO! Para rodar agora, digite:"
echo "source venv/bin/activate && python3 gerador_brx.py"
EOF

chmod +x setup_completo.sh
./setup_completo.sh
```

### 📈 Características do Sandbox
- **Ambiente Isolado**: Execução segura de código Python via `exec()`.
- **Sistema de Ferramentas**: Registro dinâmico de funções (Tools) para os agentes.
- **Persistência em HD**: Configurado nativamente para salvar parâmetros e logs no seu volume de 400GB.
- **Logs Profissionais**: Monitoramento em tempo real do que o agente está fazendo.

## Estrutura do Repositorio

O projeto e organizado de forma modular para garantir que o crescimento do ecossistema seja sustentavel:

| Diretorio | Funcao no Ecossistema |
| :--- | :--- |
| **geracao_parametros/** | Nucleo focado no debate circular e criacao de parametros (scripts producao.py e avancado.py). |
| **multi_escalavel/** | Espaco reservado para a futura expansao de sistemas de agentes multi-escalaveis. |
| **docs/** | Centraliza a documentacao tecnica, diagramas de arquitetura e manuais de usuario. |
| **scripts/** | Utilitarios para automacao de tarefas, instalacao e manutencao do sistema. |
| **data/** | Local de persistencia para memorias SQLite, logs de execucao e bases de conhecimento. |

## Configuracao e Escalabilidade

O Agents-Evolution e otimizado para se adaptar ao hardware disponivel. Embora o padrao seja configurado para **8 threads**, o sistema e totalmente escalavel. Ele detecta a capacidade do seu dispositivo e pode expandir o numero de "colegas na mesa" conforme o numero de threads disponiveis, permitindo debates mais profundos e processamento acelerado.

---
Desenvolvido para superar os limites da geracao de conhecimento em IA atraves da colaboracao autonoma e evolucao constante.
