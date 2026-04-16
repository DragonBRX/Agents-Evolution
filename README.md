# 🧠 Sistema Multi-Agente Inteligente v5.0

Sistema de treinamento com 8 mentes autônomas que debatem para gerar parâmetros inteligentes.

## 📁 Arquivos

| Arquivo | Descrição | Tamanho Aprox. |
|---------|-----------|----------------|
| `sistema_agentes_v5_producao.py` | **Arquivo principal** - Copie e cole no terminal | ~1.500 linhas |
| `sistema_agentes_v5_avancado.py` | Extensões: API, CLI, Visualização | ~800 linhas |

## 🚀 Uso Rápido

### 1. Instalar dependências (opcional mas recomendado)

```bash
pip install requests beautifulsoup4 colorama
```

### 2. Executar o sistema

```bash
# Download do arquivo
wget https://seu-link/sistema_agentes_v5_producao.py

# Executar diretamente
python3 sistema_agentes_v5_producao.py
```

Ou **copie e cole** todo o conteúdo do arquivo em um terminal Python.

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                             │
│              (Coordena execução completa)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 8 Agentes    │ │ SalaDebate   │ │   Banco de   │
│ Autônomos    │ │ (Críticas)   │ │   Dados      │
│              │ │              │ │  (SQLite)    │
│ • Designer   │ │              │ │              │
│ • Analista   │ │              │ │              │
│ • Criador    │ │              │ │              │
│ • Crítico    │ │              │ │              │
│ • Revisor    │ │              │ │              │
│ • Validador  │ │              │ │              │
│ • Estrategista│ │              │ │              │
│ • Memória    │ │              │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
```

## 🧩 Os 8 Agentes

| # | Agente | Especialidade | Personalidade |
|---|--------|---------------|---------------|
| 1 | **Designer** | Estrutura e padrões visuais | Criativo (0.9) |
| 2 | **Analista** | Métricas e dados | Rigoroso (0.95) |
| 3 | **Criador** | Geração de ideias | Muito criativo (0.95) |
| 4 | **Crítico** | Identificação de falhas | Muito rigoroso (0.95) |
| 5 | **Revisor** | Refinamento textual | Equilibrado |
| 6 | **Validador** | Verificação de coerência | Rigoroso |
| 7 | **Estrategista** | Planejamento | Estratégico |
| 8 | **Memória** | Armazenamento de padrões | Conservador |

## 📊 Funcionalidades

### Core (sistema_agentes_v5_producao.py)

- ✅ **8 Agentes autônomos** com personalidades únicas
- ✅ **Debate em múltiplas rodadas** (5-50 rodadas)
- ✅ **Geração de parâmetros** (positivos/negativos/incertos)
- ✅ **Banco de dados SQLite** com SQLAlchemy-style
- ✅ **Busca web** (DuckDuckGo)
- ✅ **Memória persistente** entre execuções
- ✅ **Auto-melhoria** baseada em parâmetros anteriores
- ✅ **Processamento paralelo** (8 threads)

### Avançado (sistema_agentes_v5_avancado.py)

- 🔷 **CLI Interativo** - Interface de comandos
- 🔷 **API REST** (Flask) - Endpoints HTTP
- 🔷 **Exportação** - JSON, HTML, CSV
- 🔷 **Visualização** - Gráficos e dashboards
- 🔷 **Relatórios** - HTML interativo

## 💻 Exemplos de Uso

### Uso Básico

```python
# No arquivo principal
from sistema_agentes_v5_producao import main

# Executar com padrões
resultados = main()

# Customizar
resultados = main(
    topicos=["python_avancado", "machine_learning"],
    num_rodadas=20,
    usar_web_search=True
)
```

### CLI Interativo

```bash
python sistema_agentes_v5_avancado.py cli
```

Comandos disponíveis:
- `ajuda` - Mostra ajuda
- `status` - Status do sistema
- `topicos` - Lista tópicos
- `processar <topico>` - Processa tópico
- `buscar <query>` - Busca na web
- `memoria` - Mostra memória
- `exportar` - Exporta dados
- `sair` - Sai do CLI

### API REST

```bash
# Iniciar servidor
python sistema_agentes_v5_avancado.py api --port 5000

# Endpoints:
GET  /api/status              # Estatísticas
GET  /api/topicos             # Lista tópicos
POST /api/processar/<topico>  # Processa tópico
GET  /api/parametros          # Lista parâmetros
GET  /api/memoria             # Lista memória
```

### Exportar Relatórios

```bash
# HTML
python sistema_agentes_v5_avancado.py exportar --formato html

# JSON
python sistema_agentes_v5_avancado.py exportar --formato json

# Dashboard visual
python sistema_agentes_v5_avancado.py dashboard
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas

```sql
-- Parâmetros gerados
parametros (id, topico, tipo_param, conteudo, score, ...)

-- Críticas entre agentes
criticas (id, de_agente, para_agente, pontos_positivos, ...)

-- Ciclos de debate completos
ciclos_debate (id, topico, score_consenso, ...)

-- Memória global
memoria_global (id, tipo, dados, relevancia, ...)

-- Performance dos agentes
agente_performance (id, agente_nome, score_medio, ...)

-- Cache de busca web
busca_web_cache (id, query, resultados, ...)
```

## ⚙️ Configuração

Edite as constantes no início do arquivo:

```python
CONFIG = Config(
    MAX_WORKERS=8,              # Threads paralelas
    NUM_RODADAS_PADRAO=15,      # Rodadas de debate
    THRESHOLD_POSITIVO=0.7,     # Score para positivo
    THRESHOLD_NEGATIVO=0.4,     # Score para negativo
    WEB_SEARCH_ENABLED=True,    # Busca web
    ...
)
```

## 📈 Tópicos Padrão

```python
TOPICOS_PADRAO = [
    "python_avancado",
    "docker_kubernetes",
    "aws_cloud",
    "machine_learning",
    "sql_otimizado",
    "blockchain_cripto",
    "cybersecurity_defesa",
    "api_rest_graphql",
    "arquitetura_software",
    "performance_tuning",
    "devops_ci_cd",
    "microservicos"
]
```

## 🔧 Como Escalar para 1 Milhão de Linhas

Para escalar este sistema:

1. **Modularização**: Separe em múltiplos arquivos por responsabilidade
2. **Banco de Dados**: Migre para PostgreSQL
3. **Cache**: Adicione Redis para cache
4. **Fila de Tarefas**: Use Celery + RabbitMQ
5. **API**: Evolua para FastAPI async
6. **Containerização**: Docker + Kubernetes
7. **Monitoramento**: Prometheus + Grafana

## 📦 Dependências

### Obrigatórias
- Python 3.8+
- SQLite3 (built-in)

### Opcionais (recomendadas)
```
requests          # Busca web
beautifulsoup4    # Parse HTML
colorama          # Cores no terminal
flask             # API REST
matplotlib        # Visualização
pandas            # Análise de dados
numpy             # Computação numérica
```

Instale todas:
```bash
pip install requests beautifulsoup4 colorama flask matplotlib pandas numpy
```

## 🐛 Troubleshooting

### Erro: "No module named 'requests'"
```bash
pip install requests beautifulsoup4
```

### Erro: Permissão de banco de dados
```bash
# Dê permissão ao diretório
chmod -R 755 ~/sistema_agentes_inteligentes
```

### Performance lenta
- Reduza `NUM_RODADAS_PADRAO`
- Diminua `PARALELISMO_TOPICO`
- Desative `WEB_SEARCH_ENABLED`

## 📄 Licença

MIT License - Use livremente!

---

**Desenvolvido para treinamento de IA com 8 mentes colaborativas** 🧠✨
