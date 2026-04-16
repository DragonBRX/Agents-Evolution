#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    SISTEMA DE GERAÇÃO DE PARÂMETROS BRX (v5.3) - PRODUÇÃO
    Integração: 8 Mentes Autônomas (Original) + Sandbox Modular + Ferramentas AgentForge
    Otimizado para HD de 400GB em /media/dragonscp/Novo volume/modelo BRX
"""

import sys
import json
import time
import random
from pathlib import Path
from sandbox_sistema.core.sandbox import Sandbox

# ====================================================================================
# SEÇÃO 1: DEFINIÇÃO DAS 8 MENTES PROFISSIONAIS (PERSONALIDADES ORIGINAIS)
# ====================================================================================

AGENTES_BRX = {
    "Designer": {
        "especialidade": "Estrutura e Padrões de Dados",
        "objetivo": "Garantir que os parâmetros sigam uma arquitetura lógica e escalável.",
        "foco": "Estrutura JSON, esquemas de dados, organização hierárquica."
    },
    "Analista": {
        "especialidade": "Lógica e Consistência Técnica",
        "objetivo": "Validar a precisão técnica e a fundamentação lógica das informações.",
        "foco": "Cálculos, fatos científicos, rigor lógico, consistência interna."
    },
    "Inovador": {
        "especialidade": "Abordagens Criativas e Novas Perspectivas",
        "objetivo": "Expandir o conhecimento para além do óbvio, sugerindo novas conexões.",
        "foco": "Brainstorming, associações não óbvias, originalidade, tendências futuras."
    },
    "Critico": {
        "especialidade": "Identificação de Falhas e Riscos (Red Teaming)",
        "objetivo": "Atuar como o 'advogado do diabo', encontrando erros e pontos fracos.",
        "foco": "Contradições, vieses, erros de segurança, exceções não tratadas."
    },
    "Revisor": {
        "especialidade": "Qualidade Textual e Clareza de Comunicação",
        "objetivo": "Refinar a linguagem para que seja clara, profissional e sem ambiguidades.",
        "foco": "Gramática, tom de voz, coesão, fluidez textual, terminologia."
    },
    "Validador": {
        "especialidade": "Coerência Temática e Precisão de Dados",
        "objetivo": "Garantir que o conteúdo esteja alinhado com o tópico central e objetivos.",
        "foco": "Relevância, veracidade, alinhamento com a meta, utilidade prática."
    },
    "Estrategista": {
        "especialidade": "Planejamento e Utilidade dos Parâmetros",
        "objetivo": "Garantir que o parâmetro gerado tenha valor estratégico para o modelo.",
        "foco": "Aplicação prática, escalabilidade, impacto no treinamento, visão macro."
    },
    "Memoria": {
        "especialidade": "Contexto Histórico e Persistência de Dados",
        "objetivo": "Manter a continuidade do conhecimento entre os ciclos de debate.",
        "foco": "Histórico de parâmetros, referências cruzadas, armazenamento, recuperação."
    }
}

# ====================================================================================
# SEÇÃO 2: LÓGICA DE EXECUÇÃO DO DEBATE CIRCULAR (ONE-LINER STYLE)
# ====================================================================================

def main():
    # Inicializa o Sandbox (Ambiente Isolado e Robusto)
    # Aponta diretamente para o seu HD de 400GB
    sb = Sandbox("BRX_Evolution_v53", storage_path="/media/dragonscp/Novo volume/modelo BRX")
    
    print("="*80)
    print("INICIANDO MOTOR DE GERAÇÃO DE PARÂMETROS BRX v5.3")
    print(f"Armazenamento: {sb.storage_root}")
    print("="*80)

    # Tópico para a geração (Pode ser alterado ou vir de uma lista)
    topico_atual = "Sistemas Multi-Agente para Automação de Pesquisa Científica"

    # Código que será executado DENTRO do Sandbox (Isolamento Total)
    # Este código utiliza as ferramentas registradas no Sandbox (v5.3)
    codigo_debate = f"""
import json
import time

print(f"Tópico de Debate: {topico_atual}")

# 1. Simulação da Mesa de Reunião (As 8 Mentes Conversando)
debate_concluido = []
mentes = {json.dumps(AGENTES_BRX, indent=4, ensure_ascii=False)}

print("-" * 50)
for nome_agente, perfil in mentes.items():
    print(f"[Mente: {{nome_agente}}] Iniciando raciocínio...")
    
    # Simulação de Raciocínio Profundo (Inspirado no AgentForge)
    # Aqui cada agente usa sua 'especialidade' para gerar um parâmetro
    pensamento = f"Analise de {{nome_agente}}: Como especialista em {{perfil['especialidade']}}, " \\
                 f"minha contribuição para o tópico '{topico_atual}' é focar no objetivo de {{perfil['objetivo']}}."
    
    # Utiliza a ferramenta de ANALISE DE QUALIDADE (Nova no v5.3)
    metricas = analisar_qualidade(text=pensamento)
    
    # Prepara o Parâmetro Positivo
    parametro = {{
        "agente": nome_agente,
        "topico": "{topico_atual}",
        "conteudo": pensamento,
        "metricas": metricas,
        "tipo": "POSITIVO",
        "versao_sistema": "5.3.0"
    }}
    
    # Salva o Parâmetro no HD de 400GB usando a ferramenta ESCREVER_ARQUIVO
    filename = f"parametro_{{nome_agente.lower()}}_{{int(time.time())}}.json"
    status = escrever_arquivo(filename=filename, content=parametro, subdir="parametros")
    
    print(f"[OK] {{status}} (Qualidade: {{metricas['vocabulary_richness']:.2f}})")
    debate_concluido.append(parametro)

print("-" * 50)
print(f"Total de parâmetros gerados no HD: {{len(debate_concluido)}}")
"""

    # Executa o debate no Sandbox
    resultado = sb.execute(codigo_debate, context_name="debate_8_mentes")

    if resultado["success"]:
        print("\n✅ Ciclo de geração finalizado com sucesso!")
        print(f"⏱️ Tempo total: {resultado['duration']:.2f}s")
        print(f"📂 Verifique os arquivos em: {sb.storage_root}/parametros/")
    else:
        print("\n❌ Falha na geração de parâmetros:")
        print(resultado["error"])

if __name__ == "__main__":
    main()
EOF
