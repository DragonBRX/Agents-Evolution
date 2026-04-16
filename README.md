# 🧠 Agents-Evolution

**Agents-Evolution** é um ecossistema de inteligência coletiva circular projetado para a geração de parâmetros inteligentes através do debate colaborativo entre múltiplas mentes autônomas. O sistema opera sob o conceito de uma mesa de reunião virtual, onde agentes especializados discutem e refinam informações para alcançar um consenso de alta qualidade.

## 🚀 O Conceito: Debate Circular e Evolução

O modelo de funcionamento do **Agents-Evolution** rompe com as abordagens tradicionais de processamento linear. Em vez disso, ele utiliza um sistema de **Threads Colaborativas**, onde o processamento é distribuído entre múltiplas threads — por padrão, 8 mentes — que atuam como colegas em uma mesa de conferência. Essas informações, coletadas via busca web ou bases locais, circulam entre os agentes em um fluxo contínuo de refinamento, onde cada especialista contribui com sua perspectiva única até que um acordo superior seja estabelecido.

Diferente de sistemas que dependem de pontuações numéricas fixas, este modelo foca na polaridade dos parâmetros para guiar o aprendizado:

| Tipo de Parâmetro | Descrição e Objetivo |
| :--- | :--- |
| **Positivos** | Respostas ideais e comportamentos desejados que o modelo deve priorizar e replicar. |
| **Negativos** | Respostas falhas, imprecisões ou comportamentos que devem ser ativamente evitados. |

Esta abordagem permite uma **Evolução por Nível** contínua. À medida que o sistema amadurece, o conhecimento que anteriormente era considerado avançado torna-se a base de sustentação para novos patamares de inteligência. O modelo evolui para superar seus próprios parâmetros anteriores, criando um ciclo de auto-melhoria constante.

## 📂 Estrutura do Repositório

O projeto é organizado de forma modular para garantir que o crescimento do ecossistema seja sustentável e organizado. Cada diretório possui uma responsabilidade clara dentro do fluxo de trabalho dos agentes:

| Diretório | Função no Ecossistema |
| :--- | :--- |
| **`geracao_parametros/`** | Contém o núcleo atual focado no debate circular e criação de parâmetros (scripts `producao.py` e `avancado.py`). |
| **`multi_escalavel/`** | Espaço reservado para a futura expansão e integração de sistemas de agentes multi-escaláveis. |
| **`docs/`** | Centraliza a documentação técnica, diagramas de arquitetura e manuais de usuário. |
| **`scripts/`** | Repositório de utilitários para automação de tarefas, instalação e manutenção do sistema. |
| **`data/`** | Local de persistência para memórias SQLite, logs de execução e bases de conhecimento acumuladas. |

## ⚙️ Configuração e Escalabilidade

O **Agents-Evolution** é otimizado para se adaptar ao hardware disponível no dispositivo de execução. Embora o padrão de operação seja configurado para **8 threads (8 mentes)**, o sistema é totalmente escalável. Ele pode ser ajustado para utilizar o número máximo de threads que o processador suportar, permitindo debates mais profundos ou processamento acelerado de grandes volumes de dados conforme a necessidade do projeto.

---
**Desenvolvido para superar os limites da geração de conhecimento em IA através da colaboração autônoma.**
