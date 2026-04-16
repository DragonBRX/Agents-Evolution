# 🧠 Sistema de Agentes Inteligentes

Repositório para o desenvolvimento e orquestração de sistemas multi-agentes avançados.

## 📂 Estrutura do Projeto

O projeto foi organizado de forma modular para eliminar redundâncias e preparar o ambiente para futuras expansões:

- **`geracao_parametros/`**: Módulo atual focado na geração de parâmetros inteligentes via debate multi-agente.
  - `producao.py`: Script principal otimizado para execução.
  - `avancado.py`: Extensões para CLI, API REST e visualização de dados.
  - `core/`: Estrutura interna de agentes, configurações e utilitários.
- **`multi_escalavel/`**: Diretório reservado para o futuro sistema de agentes multi-escaláveis.
- **`docs/`**: Documentação técnica, diagramas e manuais.
- **`scripts/`**: Scripts de automação, instalação e manutenção.
- **`data/`**: Diretório para persistência de dados, memórias SQLite e logs.
- **`tests/`**: Testes unitários e de integração.

## 🚀 Como Iniciar

Para utilizar o sistema de geração de parâmetros:

1. Navegue até a pasta `geracao_parametros/`.
2. Instale as dependências: `pip install requests beautifulsoup4 colorama flask matplotlib pandas numpy`.
3. Execute o núcleo do sistema: `python producao.py`.

---
**Este repositório é mantido com foco em código limpo, sem numeração de versões nos arquivos e com separação clara de responsabilidades.**
