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
