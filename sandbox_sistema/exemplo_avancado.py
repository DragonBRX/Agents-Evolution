#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    EXEMPLO AVANÇADO: AGENTE COM MÚLTIPLAS FERRAMENTAS
    Demonstra um agente executando tarefas complexas dentro do sandbox.
"""

import json
import time
from core.sandbox import Sandbox

def criar_agente_pesquisa():
    """Cria um agente de pesquisa com ferramentas especializadas."""
    
    agente = Sandbox("AgentePesquisador")
    
    # ===== FERRAMENTAS ESPECIALIZADAS =====
    
    def ferramenta_busca_web(query: str, max_resultados: int = 3):
        """Busca simulada na web com múltiplos resultados."""
        print(f"[BUSCA] Pesquisando: {query}")
        resultados = [
            {
                "titulo": f"Resultado 1: {query}",
                "url": "https://exemplo.com/1",
                "relevancia": 0.95
            },
            {
                "titulo": f"Resultado 2: {query}",
                "url": "https://exemplo.com/2",
                "relevancia": 0.87
            },
            {
                "titulo": f"Resultado 3: {query}",
                "url": "https://exemplo.com/3",
                "relevancia": 0.72
            }
        ]
        return resultados[:max_resultados]

    def ferramenta_analisar_dados(dados: dict):
        """Analisa dados e retorna estatísticas."""
        print(f"[ANÁLISE] Analisando {len(dados)} itens...")
        return {
            "total_itens": len(dados),
            "timestamp": time.time(),
            "status": "análise_concluída"
        }

    def ferramenta_gerar_relatorio(titulo: str, conteudo: str):
        """Gera um relatório estruturado."""
        print(f"[RELATÓRIO] Gerando relatório: {titulo}")
        return {
            "titulo": titulo,
            "tamanho_conteudo": len(conteudo),
            "status": "relatório_gerado",
            "timestamp": time.time()
        }

    def ferramenta_classificar_texto(texto: str):
        """Classifica um texto em categorias."""
        print(f"[CLASSIFICAÇÃO] Classificando texto...")
        categorias = ["Tecnologia", "Negócios", "Educação", "Saúde", "Outro"]
        return {
            "categoria_principal": categorias[0],
            "confiança": 0.92,
            "categorias_alternativas": categorias[1:3]
        }

    # Registra todas as ferramentas
    agente.register_tool("busca_web", ferramenta_busca_web, "Busca na internet por informações.")
    agente.register_tool("analisar", ferramenta_analisar_dados, "Analisa dados e gera estatísticas.")
    agente.register_tool("gerar_relatorio", ferramenta_gerar_relatorio, "Cria um relatório estruturado.")
    agente.register_tool("classificar", ferramenta_classificar_texto, "Classifica texto em categorias.")
    
    return agente

def executar_tarefa_agente():
    """Executa uma tarefa complexa usando o agente."""
    
    print("\n" + "="*70)
    print("  EXEMPLO AVANÇADO: AGENTE DE PESQUISA EXECUTANDO TAREFA")
    print("="*70 + "\n")
    
    # Cria o agente
    agente = criar_agente_pesquisa()
    
    # Mostra ferramentas disponíveis
    print("📋 FERRAMENTAS DISPONÍVEIS NO AGENTE:")
    for tool in agente.list_tools():
        print(f"   ✓ {tool['name']}: {tool['description']}")
    
    # Código que o agente vai executar
    codigo_agente = """
import json

print("\\n🤖 AGENTE INICIANDO TAREFA DE PESQUISA\\n")

# Tarefa 1: Buscar informações
print("Etapa 1: Buscando informações sobre Inteligência Artificial...")
resultados = busca_web(query="Inteligência Artificial", max_resultados=2)
print(f"Encontrados {len(resultados)} resultados")

# Tarefa 2: Analisar dados
print("\\nEtapa 2: Analisando dados coletados...")
analise = analisar(dados={"resultados": resultados})
print(f"Análise concluída: {analise['status']}")

# Tarefa 3: Classificar conteúdo
print("\\nEtapa 3: Classificando conteúdo...")
classificacao = classificar(texto="Inteligência Artificial e Machine Learning")
print(f"Categoria: {classificacao['categoria_principal']} (Confiança: {classificacao['confiança']})")

# Tarefa 4: Gerar relatório
print("\\nEtapa 4: Gerando relatório final...")
relatorio = gerar_relatorio(
    titulo="Relatório de Pesquisa - IA",
    conteudo=json.dumps(resultados, indent=2)
)
print(f"Relatório gerado: {relatorio['titulo']}")

print("\\n✅ TODAS AS TAREFAS CONCLUÍDAS COM SUCESSO!")
"""
    
    # Adiciona json ao ambiente
    agente.locals_env['json'] = json
    
    # Executa o código
    resultado = agente.run_code(codigo_agente)
    
    # Exibe resultado
    print("\n" + "-"*70)
    print("📊 RESULTADO DA EXECUÇÃO:")
    print("-"*70)
    print(f"Status: {'✅ Sucesso' if resultado['success'] else '❌ Falha'}")
    print(f"Tempo de execução: {resultado['execution_time']}")
    
    if resultado['output']:
        print("\n📝 Saída do Agente:")
        print(resultado['output'])
    
    if resultado['error']:
        print("\n⚠️ Erros encontrados:")
        print(resultado['error'])
    
    print("\n" + "="*70)
    print("📈 ESTATÍSTICAS DE USO DAS FERRAMENTAS:")
    print("="*70)
    for tool in agente.list_tools():
        print(f"   {tool['name']}: Usada {tool['usage_count']} vez(es)")

if __name__ == "__main__":
    executar_tarefa_agente()
