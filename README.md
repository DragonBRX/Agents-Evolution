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

## Novidade: Autonomia Real e Memoria Evolutiva

O ecossistema agora integra capacidades de Autonomia Real, permitindo que as 8 mentes profissionais evoluam sozinhas a cada ciclo de geracao.

### Caracteristicas da Autonomia
- **8 Mentes Profissionais Preservadas**: Designer, Analista, Inovador, Critico, Revisor, Validador, Estrategista e Memoria.
- **Memoria Evolutiva**: Os agentes acessam o que ja aprenderam no HD de 400GB para construir sobre acertos e evitar erros passados.
- **Auto-Reflexao**: Cada agente avalia a qualidade do proprio raciocinio antes de finalizar um parametro.
- **Aprendizado Recurvado**: O sistema registra "licoes aprendidas" que sao consultadas em ciclos futuros de debate.
- **Persistencia Nativa em HD**: Totalmente configurado para o seu volume de 400GB (/media/dragonscp/Novo volume/modelo BRX).

### Instalacao Ultra-Rapida (Ubuntu) - Focada em Performance

Se o seu sistema ja tem o Python instalado, este comando e muito mais rapido e pula as atualizacoes pesadas do Ubuntu:

```bash
# 1. Baixe e execute o setup ultra-rapido (Pula apt update)
curl -O https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/setup_rapido.sh && chmod +x setup_rapido.sh && ./setup_rapido.sh
```

### Setup Completo (Para Sistemas Novos)

Para uma instalacao que inclui todas as dependencias do sistema operacional (pode ser mais lenta):

```bash
# 1. Baixe e execute o script mestre de configuracao completa
curl -O https://raw.githubusercontent.com/DragonBRX/Agents-Evolution/main/setup_completo.sh && chmod +x setup_completo.sh && ./setup_completo.sh
```

### Como Executar a Geracao de Parametros

Apos o setup rapido, o sistema inicia a geracao automaticamente. Para rodar novamente:
```bash
cd ~/Agents-Evolution-Sandbox
./run.sh
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
