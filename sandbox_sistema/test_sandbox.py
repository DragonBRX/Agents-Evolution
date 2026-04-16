#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    TESTE DO AMBIENTE SANDBOX MODULAR
    Verifica registro de ferramentas, execução de código, logs e erros.
"""

import os
import json
from core.sandbox import Sandbox

def run_tests():
    print("\n🚀 INICIANDO TESTES DO AMBIENTE SANDBOX\n")
    
    # 1. Inicializa o Sandbox
    sb = Sandbox("AgenteEvolution_Sandbox")
    
    # 2. Define e Registra Ferramentas (Simples e Úteis)
    
    def ferramenta_busca_fake(query: str):
        """Simula uma busca na internet."""
        print(f"[TOOL] Buscando na web por: {query}")
        return {
            "query": query,
            "resultados": [
                {"titulo": f"Artigo sobre {query}", "url": f"https://exemplo.com/{query}"},
                {"titulo": f"Notícia: {query} em alta", "url": f"https://noticias.com/{query}"}
            ]
        }
    
    def ferramenta_arquivo_fake(nome: str, conteudo: str):
        """Simula a escrita de um arquivo."""
        print(f"[TOOL] Escrevendo arquivo '{nome}'...")
        # Apenas simula, não escreve de verdade para manter o ambiente limpo
        return f"Arquivo '{nome}' salvo com sucesso (Simulado)."

    # Registro no Sandbox
    sb.register_tool("busca", ferramenta_busca_fake, "Realiza buscas simuladas na internet.")
    sb.register_tool("salvar_arquivo", ferramenta_arquivo_fake, "Simula o salvamento de arquivos locais.")

    print("\n--- TESTE 1: EXECUÇÃO SIMPLES ---")
    codigo_1 = """
print('Iniciando tarefa de pesquisa...')
info = busca(query='Python Sandbox')
print(f'Encontrados {len(info["resultados"])} resultados.')
print(f'Primeiro resultado: {info["resultados"][0]["titulo"]}')
"""
    res1 = sb.run_code(codigo_1)
    
    print("\n--- TESTE 2: MÚLTIPLAS FERRAMENTAS ---")
    codigo_2 = """
print('Processando dados e salvando relatório...')
resultado_busca = busca(query='IA Generativa')
relatorio = f"Relatório de IA: {json.dumps(resultado_busca)}"
status = salvar_arquivo(nome='relatorio_ia.txt', conteudo=relatorio)
print(f'Status final: {status}')
"""
    # Adicionando json ao ambiente local para o código acima funcionar
    sb.locals_env['json'] = json
    res2 = sb.run_code(codigo_2)

    print("\n--- TESTE 3: TRATAMENTO DE ERROS ---")
    codigo_erro = """
print('Tentando operação inválida...')
x = 10 / 0  # ZeroDivisionError
print('Isso não será executado.')
"""
    res3 = sb.run_code(codigo_erro)

    print("\n--- RESUMO DOS RESULTADOS ---")
    print(f"Execução 1 (Simples): {'Sucesso' if res1['success'] else 'Falha'}")
    print(f"Execução 2 (Ferramentas): {'Sucesso' if res2['success'] else 'Falha'}")
    print(f"Execução 3 (Erro): {'Sucesso' if res3['success'] else 'Falha (Esperado)'}")
    
    print("\n--- LISTA DE FERRAMENTAS NO SANDBOX ---")
    for tool in sb.list_tools():
        print(f"- {tool['name']}: {tool['description']} (Usada {tool['usage_count']} vezes)")

if __name__ == "__main__":
    run_tests()
