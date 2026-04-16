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

## Novidade: Sandbox Modular e Raciocinio Avancado (v5.2)

Agora o ecossistema integra as melhores logicas de raciocinio e ferramentas inspiradas no **AgentForge**, focando 100% na qualidade e profundidade dos parametros gerados para o seu futuro modelo.

### Caracteristicas da Versao 5.2
- **8 Mentes Profissionais**: Cada uma com uma especialidade distinta (Designer, Analista, Inovador, Critico, Revisor, Validador, Estrategista e Memoria).
- **Raciocinio Multi-Perspectiva**: Cada agente analisa o topico sob sua propria otica tecnica, garantindo uma cobertura completa.
- **Ferramentas Avancadas**: Integracao de Shell, Arquivos, Analise de Texto e Metricas de Qualidade diretamente no Sandbox.
- **Persistencia em HD**: Otimizado para salvar parametros estruturados em JSON no seu volume de 400GB (/media/dragonscp/Novo volume/modelo BRX).

### Instalacao Rapida (Ubuntu) - Setup Completo em 1 Comando

Para configurar todo o ambiente no seu Ubuntu, incluindo a criacao de diretorios no HD externo, instalacao de dependencias do sistema e bibliotecas Python, execute o bloco abaixo no seu terminal:

```bash
# 1. Baixe e execute o script mestre de configuracao v5.2
curl -O https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/setup_completo.sh 2>/dev/null || cat << 'EOF' > setup_completo.sh
#!/bin/bash
set -e
echo "INICIANDO SETUP COMPLETO NO HD DE 400GB (v5.2)..."
STORAGE_ROOT="/media/dragonscp/Novo volume/modelo BRX"
PROJECT_DIR="$HOME/Agents-Evolution-Sandbox"
sudo mkdir -p "$STORAGE_ROOT/dados" "$STORAGE_ROOT/logs" "$STORAGE_ROOT/parametros"
sudo chown -R $USER:$USER "$STORAGE_ROOT"
sudo apt update -y && sudo apt install -y python3 python3-pip python3-venv git libsqlite3-dev
mkdir -p "$PROJECT_DIR/core" && cd "$PROJECT_DIR"
python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip && pip install requests beautifulsoup4 colorama flask matplotlib numpy pandas sqlalchemy
cat << 'CORE' > core/sandbox.py
import sys, json, logging, traceback, io, contextlib, subprocess
from typing import Dict, Any, List, Callable
from datetime import datetime
from pathlib import Path
class Sandbox:
    def __init__(self, name="BRX_Sandbox", storage="/media/dragonscp/Novo volume/modelo BRX"):
        self.name = name
        self.storage = Path(storage)
        self.tools = {}
        self.globals_env = {"__builtins__": __builtins__}
        self.locals_env = {"print": self._print, "datetime": datetime, "json": json, "storage_path": str(self.storage)}
        self._ensure_storage()
        self._register_default_tools()
    def _ensure_storage(self):
        self.storage.mkdir(parents=True, exist_ok=True)
        print(f"DEBUG: Armazenamento em {self.storage}")
    def _print(self, *args):
        print(f"[{self.name}] {' '.join(map(str, args))}")
    def register_tool(self, name, func):
        self.tools[name] = func
        self.locals_env[name] = func
    def _register_default_tools(self):
        def execute_shell(command):
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
                return {"stdout": result.stdout, "stderr": result.stderr, "code": result.returncode}
            except Exception as e: return {"error": str(e)}
        def read_file(path):
            full_path = self.storage / path
            if not full_path.exists(): return f"Erro: Arquivo {path} nao encontrado."
            return full_path.read_text(encoding='utf-8')
        def write_file(path, content):
            full_path = self.storage / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
            return f"Sucesso: {path} salvo."
        def analyze_text(text):
            words = text.split()
            return {"word_count": len(words), "char_count": len(text), "unique_words": len(set(w.lower() for w in words)), "complexity": len(set(words)) / max(1, len(words))}
        self.register_tool("shell", execute_shell)
        self.register_tool("ler_arquivo", read_file)
        self.register_tool("escrever_arquivo", write_file)
        self.register_tool("analisar_texto", analyze_text)
    def run(self, code):
        try:
            exec(code, self.globals_env, self.locals_env)
            return True
        except Exception:
            print(traceback.format_exc()); return False
CORE
cat << 'GEN' > gerador_brx.py
from core.sandbox import Sandbox
import time, json
def main():
    sb = Sandbox("Gerador_BRX")
    def salvar_conhecimento(tipo, topico, conteudo):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        data = {"timestamp": timestamp, "tipo": tipo, "topico": topico, "conteudo": conteudo}
        filename = f"parametros/{topico}_{int(time.time())}.json"
        sb.locals_env["escrever_arquivo"](filename, json.dumps(data, indent=4, ensure_ascii=False))
        return f"Parametro {tipo} salvo em {filename}"
    sb.register_tool("salvar_conhecimento", salvar_conhecimento)
    codigo = "print('Iniciando Evolucao de Parametros BRX...'); status = salvar_conhecimento('POSITIVO', 'Arquitetura_IA', 'Nova logica detectada.'); print(f'Status do HD: {status}')"
    sb.run(codigo)
if __name__ == "__main__": main()
GEN
echo "SETUP CONCLUIDO! Para rodar agora, digite:"
echo "source venv/bin/activate && python3 gerador_brx.py"
EOF

chmod +x setup_completo.sh
./setup_completo.sh
```

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

O Agents-Evolution e otimizado para se adaptar ao hardware disponivel. Embora o padrao seja configurado para 8 threads, o sistema e totalmente escalavel. Ele detecta a capacidade do seu dispositivo e pode expandir o numero de "colegas na mesa" conforme o numero de threads disponiveis, permitindo debates mais profundos e processamento acelerado.

---
Desenvolvido para superar os limites da geracao de conhecimento em IA atraves da colaboracao autonoma e evolucao constante.
