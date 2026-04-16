#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   SISTEMA MULTI-AGENTE INTELIGENTE v5.0 - MÓDULO AVANÇADO                        ║
║   Extensões: API REST, CLI Interativo, Visualização, Exportação                  ║
║                                                                                  ║
║   Use este arquivo junto com o sistema_agentes_v5_producao.py                    ║
║   ou combine ambos em um único arquivo maior                                     ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

# ====================================================================================
# IMPORTS ADICIONAIS PARA FUNCIONALIDADES AVANÇADAS
# ====================================================================================

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Tentativa de imports opcionais
try:
    from flask import Flask, jsonify, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# ====================================================================================
# CLI INTERATIVO
# ====================================================================================

class CLIInterativo:
    """Interface de linha de comando interativa."""
    
    def __init__(self):
        self.comandos = {
            'ajuda': self.cmd_ajuda,
            'status': self.cmd_status,
            'topicos': self.cmd_topicos,
            'processar': self.cmd_processar,
            'buscar': self.cmd_buscar,
            'memoria': self.cmd_memoria,
            'exportar': self.cmd_exportar,
            'visualizar': self.cmd_visualizar,
            'limpar': self.cmd_limpar,
            'sair': self.cmd_sair
        }
    
    def iniciar(self):
        """Inicia CLI interativo."""
        print("\n" + "="*60)
        print("  SISTEMA MULTI-AGENTE - CLI INTERATIVO")
        print("="*60)
        print("  Digite 'ajuda' para ver os comandos disponíveis\n")
        
        while True:
            try:
                comando = input("agente> ").strip().lower()
                partes = comando.split()
                
                if not partes:
                    continue
                
                cmd = partes[0]
                args = partes[1:]
                
                if cmd in self.comandos:
                    self.comandos[cmd](args)
                else:
                    print(f"❌ Comando desconhecido: {cmd}")
                    print("   Digite 'ajuda' para ver os comandos")
                    
            except KeyboardInterrupt:
                print("\n👋 Saindo...")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
    
    def cmd_ajuda(self, args):
        """Mostra ajuda."""
        print("\n📖 COMANDOS DISPONÍVEIS:")
        print("-" * 40)
        print("  ajuda              - Mostra esta ajuda")
        print("  status             - Status do sistema")
        print("  topicos            - Lista tópicos disponíveis")
        print("  processar <topico> - Processa um tópico")
        print("  buscar <query>     - Busca na web")
        print("  memoria [topico]   - Mostra memória")
        print("  exportar [formato] - Exporta dados")
        print("  visualizar         - Gera visualizações")
        print("  limpar             - Limpa dados antigos")
        print("  sair               - Sai do CLI")
        print()
    
    def cmd_status(self, args):
        """Mostra status do sistema."""
        try:
            from sistema_agentes_v5_producao import db
            stats = db.get_estatisticas()
            
            print("\n📊 STATUS DO SISTEMA:")
            print("-" * 40)
            print(f"  📦 Parâmetros: {stats['total_parametros']}")
            print(f"  🗣️  Críticas: {stats['total_criticas']}")
            print(f"  🧠 Memórias: {stats['total_memorias']}")
            print(f"  📊 Debates: {stats['total_debates']}")
            print(f"  ⭐ Score médio: {stats['score_medio_geral']:.4f}")
            print()
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def cmd_topicos(self, args):
        """Lista tópicos."""
        topicos = [
            "python_avancado", "docker_kubernetes", "aws_cloud",
            "machine_learning", "sql_otimizado", "blockchain_cripto",
            "cybersecurity_defesa", "api_rest_graphql", "arquitetura_software",
            "performance_tuning", "devops_ci_cd", "microservicos"
        ]
        print("\n📋 TÓPICOS DISPONÍVEIS:")
        print("-" * 40)
        for i, t in enumerate(topicos, 1):
            print(f"  {i:2}. {t}")
        print()
    
    def cmd_processar(self, args):
        """Processa um tópico."""
        if not args:
            print("❌ Uso: processar <topico>")
            return
        
        topico = args[0]
        print(f"\n🚀 Processando: {topico}")
        
        try:
            from sistema_agentes_v5_producao import ProcessadorTopico
            processador = ProcessadorTopico()
            resultado = processador.processar(topico)
            
            print(f"\n✅ Concluído!")
            print(f"   Score: {resultado['score_consenso']:.2%}")
            print(f"   Parâmetros: +{resultado['parametros']['positivos']} "
                  f"-{resultado['parametros']['negativos']} "
                  f"?{resultado['parametros']['incertos']}")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def cmd_buscar(self, args):
        """Busca na web."""
        if not args:
            print("❌ Uso: buscar <query>")
            return
        
        query = ' '.join(args)
        print(f"\n🔍 Buscando: {query}")
        
        try:
            from sistema_agentes_v5_producao import web_search
            resultados = web_search.buscar(query)
            
            print(f"\n✅ {len(resultados)} resultados:")
            for i, r in enumerate(resultados[:5], 1):
                print(f"\n  {i}. {r['titulo']}")
                print(f"     {r['snippet'][:100]}...")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def cmd_memoria(self, args):
        """Mostra memória."""
        topico = args[0] if args else None
        
        try:
            from sistema_agentes_v5_producao import db
            memorias = db.recuperar_memoria(topico=topico, limit=10)
            
            print(f"\n🧠 MEMÓRIA ({len(memorias)} entradas):")
            print("-" * 40)
            for m in memorias[:5]:
                print(f"  • [{m['tipo']}] Relevância: {m['relevancia']:.2f}")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def cmd_exportar(self, args):
        """Exporta dados."""
        formato = args[0] if args else 'json'
        
        try:
            from sistema_agentes_v5_producao import db, CONFIG
            
            parametros = db.buscar_parametros(limit=1000)
            
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{formato}"
            filepath = CONFIG.SAIDA_DIR / filename
            
            if formato == 'json':
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(parametros, f, indent=2, ensure_ascii=False)
            elif formato == 'csv' and PANDAS_AVAILABLE:
                df = pd.DataFrame(parametros)
                df.to_csv(filepath, index=False)
            
            print(f"\n✅ Exportado: {filepath}")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def cmd_visualizar(self, args):
        """Gera visualizações."""
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib não instalado")
            return
        
        try:
            from sistema_agentes_v5_producao import db, CONFIG
            
            parametros = db.buscar_parametros(limit=1000)
            
            if not parametros:
                print("❌ Nenhum parâmetro para visualizar")
                return
            
            # Gráfico de distribuição de scores
            scores = [p['score'] for p in parametros]
            tipos = [p['tipo'] for p in parametros]
            
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            
            # Histograma de scores
            axes[0].hist(scores, bins=20, edgecolor='black', alpha=0.7)
            axes[0].set_xlabel('Score')
            axes[0].set_ylabel('Frequência')
            axes[0].set_title('Distribuição de Scores')
            axes[0].axvline(0.7, color='g', linestyle='--', label='Positivo')
            axes[0].axvline(0.4, color='r', linestyle='--', label='Negativo')
            axes[0].legend()
            
            # Contagem por tipo
            tipo_counts = {}
            for t in tipos:
                tipo_counts[t] = tipo_counts.get(t, 0) + 1
            
            axes[1].bar(tipo_counts.keys(), tipo_counts.values(), color=['green', 'red', 'orange'])
            axes[1].set_xlabel('Tipo')
            axes[1].set_ylabel('Quantidade')
            axes[1].set_title('Parâmetros por Tipo')
            
            plt.tight_layout()
            
            filepath = CONFIG.SAIDA_DIR / f"visualizacao_{int(time.time())}.png"
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"\n✅ Visualização salva: {filepath}")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def cmd_limpar(self, args):
        """Limpa dados antigos."""
        print("\n⚠️  Função não implementada nesta versão")
        print("   Use SQL diretamente no banco SQLite")
    
    def cmd_sair(self, args):
        """Sai do CLI."""
        print("\n👋 Até logo!")
        sys.exit(0)


# ====================================================================================
# API REST SIMPLES (Flask)
# ====================================================================================

def criar_api() -> Optional['Flask']:
    """Cria aplicação Flask para API REST."""
    if not FLASK_AVAILABLE:
        print("❌ Flask não instalado. Instale com: pip install flask")
        return None
    
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({
            'nome': 'Sistema Multi-Agente API',
            'versao': '5.0.0',
            'endpoints': [
                '/api/status',
                '/api/topicos',
                '/api/processar/<topico>',
                '/api/parametros',
                '/api/memoria'
            ]
        })
    
    @app.route('/api/status')
    def status():
        try:
            from sistema_agentes_v5_producao import db
            stats = db.get_estatisticas()
            return jsonify(stats)
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    @app.route('/api/topicos')
    def topicos():
        topicos = [
            "python_avancado", "docker_kubernetes", "aws_cloud",
            "machine_learning", "sql_otimizado", "blockchain_cripto",
            "cybersecurity_defesa", "api_rest_graphql", "arquitetura_software"
        ]
        return jsonify({'topicos': topicos})
    
    @app.route('/api/processar/<topico>', methods=['POST'])
    def processar(topico):
        try:
            from sistema_agentes_v5_producao import ProcessadorTopico
            
            num_rodadas = request.json.get('rodadas', 15) if request.json else 15
            
            processador = ProcessadorTopico()
            resultado = processador.processar(topico, num_rodadas)
            
            return jsonify(resultado)
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    @app.route('/api/parametros')
    def parametros():
        try:
            from sistema_agentes_v5_producao import db
            
            topico = request.args.get('topico')
            tipo = request.args.get('tipo')
            limit = int(request.args.get('limit', 100))
            
            params = db.buscar_parametros(topico=topico, tipo=tipo, limit=limit)
            return jsonify({'parametros': params})
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    @app.route('/api/memoria')
    def memoria():
        try:
            from sistema_agentes_v5_producao import db
            
            topico = request.args.get('topico')
            limit = int(request.args.get('limit', 50))
            
            mem = db.recuperar_memoria(topico=topico, limit=limit)
            return jsonify({'memoria': mem})
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    
    return app


def iniciar_api(host='0.0.0.0', port=5000):
    """Inicia servidor API."""
    app = criar_api()
    if app:
        print(f"🚀 API iniciando em http://{host}:{port}")
        app.run(host=host, port=port, debug=False)


# ====================================================================================
# EXPORTADOR DE RELATÓRIOS
# ====================================================================================

class ExportadorRelatorios:
    """Exporta relatórios em vários formatos."""
    
    def __init__(self):
        from sistema_agentes_v5_producao import CONFIG
        self.output_dir = CONFIG.SAIDA_DIR
    
    def exportar_json(self, filename: str = None) -> Path:
        """Exporta para JSON."""
        from sistema_agentes_v5_producao import db
        
        parametros = db.buscar_parametros(limit=10000)
        
        if not filename:
            filename = f"relatorio_{int(time.time())}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'exportado_em': datetime.now().isoformat(),
                'total': len(parametros),
                'parametros': parametros
            }, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def exportar_html(self, filename: str = None) -> Path:
        """Exporta para HTML."""
        from sistema_agentes_v5_producao import db
        
        parametros = db.buscar_parametros(limit=1000)
        stats = db.get_estatisticas()
        
        if not filename:
            filename = f"relatorio_{int(time.time())}.html"
        
        filepath = self.output_dir / filename
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Relatório Sistema Multi-Agente</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .stats {{ background: #f0f0f0; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .parametro {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .positivo {{ border-left: 4px solid green; }}
        .negativo {{ border-left: 4px solid red; }}
        .incerto {{ border-left: 4px solid orange; }}
        .score {{ font-weight: bold; }}
    </style>
</head>
<body>
    <h1>📊 Relatório Sistema Multi-Agente</h1>
    <p>Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="stats">
        <h2>Estatísticas</h2>
        <p>📦 Parâmetros: {stats['total_parametros']}</p>
        <p>🗣️ Críticas: {stats['total_criticas']}</p>
        <p>🧠 Memórias: {stats['total_memorias']}</p>
        <p>📊 Debates: {stats['total_debates']}</p>
        <p>⭐ Score Médio: {stats['score_medio_geral']:.4f}</p>
    </div>
    
    <h2>Parâmetros Recentes</h2>
"""
        
        for p in parametros[:50]:
            css_class = p['tipo']
            html += f"""
    <div class="parametro {css_class}">
        <strong>{p['topico']}</strong> | 
        <span class="score">Score: {p['score']:.4f}</span> |
        <span>Tipo: {p['tipo']}</span>
    </div>
"""
        
        html += """
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath
    
    def gerar_dashboard(self) -> Path:
        """Gera dashboard HTML interativo."""
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        from sistema_agentes_v5_producao import db, CONFIG
        
        parametros = db.buscar_parametros(limit=1000)
        
        if not parametros:
            return None
        
        # Gráficos
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Distribuição de scores
        scores = [p['score'] for p in parametros]
        axes[0, 0].hist(scores, bins=20, edgecolor='black', alpha=0.7, color='skyblue')
        axes[0, 0].set_title('Distribuição de Scores')
        axes[0, 0].set_xlabel('Score')
        axes[0, 0].set_ylabel('Frequência')
        
        # 2. Parâmetros por tipo
        tipo_counts = {}
        for p in parametros:
            tipo_counts[p['tipo']] = tipo_counts.get(p['tipo'], 0) + 1
        colors = {'positivo': 'green', 'negativo': 'red', 'incerto': 'orange'}
        axes[0, 1].bar(tipo_counts.keys(), tipo_counts.values(), 
                       color=[colors.get(t, 'gray') for t in tipo_counts.keys()])
        axes[0, 1].set_title('Parâmetros por Tipo')
        
        # 3. Top tópicos
        topico_counts = {}
        for p in parametros:
            topico_counts[p['topico']] = topico_counts.get(p['topico'], 0) + 1
        top_topics = sorted(topico_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        axes[1, 0].barh([t[0] for t in top_topics], [t[1] for t in top_topics])
        axes[1, 0].set_title('Top 10 Tópicos')
        
        # 4. Evolução temporal (simulada)
        axes[1, 1].plot(range(len(scores[:100])), sorted(scores[:100], reverse=True), 'b-')
        axes[1, 1].set_title('Evolução de Scores (últimos 100)')
        axes[1, 1].set_xlabel('Índice')
        axes[1, 1].set_ylabel('Score')
        
        plt.tight_layout()
        
        filepath = CONFIG.SAIDA_DIR / f"dashboard_{int(time.time())}.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath


# ====================================================================================
# FUNÇÕES DE UTILIDADE PARA LINHA DE COMANDO
# ====================================================================================

def executar_cli():
    """Executa CLI interativo."""
    cli = CLIInterativo()
    cli.iniciar()


def executar_api(host='0.0.0.0', port=5000):
    """Executa API REST."""
    iniciar_api(host, port)


def exportar_relatorio(formato='html'):
    """Exporta relatório."""
    exportador = ExportadorRelatorios()
    
    if formato == 'json':
        path = exportador.exportar_json()
    elif formato == 'html':
        path = exportador.exportar_html()
    else:
        print(f"❌ Formato desconhecido: {formato}")
        return
    
    print(f"✅ Relatório exportado: {path}")


def gerar_dashboard():
    """Gera dashboard visual."""
    exportador = ExportadorRelatorios()
    path = exportador.gerar_dashboard()
    
    if path:
        print(f"✅ Dashboard gerado: {path}")
    else:
        print("❌ Não foi possível gerar dashboard")


# ====================================================================================
# PARSER DE ARGUMENTOS
# ====================================================================================

def main():
    """Função principal para execução via linha de comando."""
    parser = argparse.ArgumentParser(
        description='Sistema Multi-Agente Inteligente v5.0'
    )
    
    subparsers = parser.add_subparsers(dest='comando', help='Comandos disponíveis')
    
    # Comando: cli
    cli_parser = subparsers.add_parser('cli', help='Inicia CLI interativo')
    
    # Comando: api
    api_parser = subparsers.add_parser('api', help='Inicia API REST')
    api_parser.add_argument('--host', default='0.0.0.0', help='Host')
    api_parser.add_argument('--port', type=int, default=5000, help='Porta')
    
    # Comando: exportar
    export_parser = subparsers.add_parser('exportar', help='Exporta relatório')
    export_parser.add_argument('--formato', default='html', choices=['json', 'html'])
    
    # Comando: dashboard
    subparsers.add_parser('dashboard', help='Gera dashboard visual')
    
    # Comando: treinar
    treinar_parser = subparsers.add_parser('treinar', help='Executa treinamento')
    treinar_parser.add_argument('--topicos', nargs='+', help='Tópicos')
    treinar_parser.add_argument('--rodadas', type=int, default=15, help='Rodadas')
    treinar_parser.add_argument('--no-web', action='store_true', help='Desativa web search')
    
    args = parser.parse_args()
    
    if args.comando == 'cli':
        executar_cli()
    elif args.comando == 'api':
        executar_api(args.host, args.port)
    elif args.comando == 'exportar':
        exportar_relatorio(args.formato)
    elif args.comando == 'dashboard':
        gerar_dashboard()
    elif args.comando == 'treinar':
        from sistema_agentes_v5_producao import main
        main(
            topicos=args.topicos,
            num_rodadas=args.rodadas,
            usar_web_search=not args.no_web
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
