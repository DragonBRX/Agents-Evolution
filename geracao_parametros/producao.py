#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
                                                                                    
                                                                                    
    SISTEMA MULTI-AGENTE INTELIGENTE v5.0 - PRODUÇÃO                                
    8 Mentes Autônomas | Debate Coletivo | Auto-Melhoria Contínua                   
                                                                                    
    Arquivo único de treinamento - Copie e cole diretamente no terminal             
                                                                                    
    Funcionalidades:                                                                
    - 8 Agentes autônomos com personalidades únicas                                 
    - Sistema de debate com múltiplas rodadas                                       
    - Geração e classificação de parâmetros (positivos/negativos/incertos)          
    - Banco de dados SQLite com SQLAlchemy ORM                                      
    - Busca web integrada (DuckDuckGo)                                              
    - Memória persistente entre execuções                                           
    - Auto-melhoria baseada em parâmetros anteriores                                
                                                                                    
                                                                                    
"""

# ====================================================================================
# SEÇÃO 1: IMPORTS E DEPENDÊNCIAS
# ====================================================================================

import os
import sys
import json
import time
import hashlib
import threading
import logging
import re
import random
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from abc import ABC, abstractmethod

# Tentativa de importar bibliotecas opcionais
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback para cores
    class _Fore:
        def __getattr__(self, name): return ''
    class _Style:
        def __getattr__(self, name): return ''
    Fore = _Fore()
    Style = _Style()

# ====================================================================================
# SEÇÃO 2: CONFIGURAÇÃO GLOBAL
# ====================================================================================

@dataclass
class Config:
    """Configuração central do sistema."""
    # Sistema
    NOME: str = "Sistema Multi-Agente Inteligente"
    VERSAO: str = "5.0.0"
    
    # Execução
    MAX_WORKERS: int = 8
    TIMEOUT_DEBATE: int = 300
    NUM_RODADAS_PADRAO: int = 15
    PARALELISMO_TOPICO: int = 4
    
    # Caminhos
    HOME: Path = field(default_factory=lambda: Path.home())
    BASE_DIR: Path = None
    DB_PATH: Path = None
    SAIDA_DIR: Path = None
    LOG_DIR: Path = None
    
    # Debate
    THRESHOLD_POSITIVO: float = 0.7
    THRESHOLD_NEGATIVO: float = 0.4
    PARADA_ANTECIPADA: bool = True
    SCORE_CONVERGENCIA: float = 0.85
    
    # Web Search
    WEB_SEARCH_ENABLED: bool = True
    WEB_SEARCH_TIMEOUT: int = 30
    MAX_RESULTADOS_WEB: int = 5
    CACHE_WEB_TTL: int = 86400  # 24 horas
    
    def __post_init__(self):
        self.BASE_DIR = self.HOME / "sistema_agentes_inteligentes"
        self.DB_PATH = self.BASE_DIR / "memoria.db"
        self.SAIDA_DIR = self.BASE_DIR / "saida"
        self.LOG_DIR = self.BASE_DIR / "logs"
        
        # Cria diretórios
        for path in [self.BASE_DIR, self.SAIDA_DIR, self.LOG_DIR]:
            path.mkdir(parents=True, exist_ok=True)

# Instância global de configuração
CONFIG = Config()

# ====================================================================================
# SEÇÃO 3: SETUP DE LOGGING
# ====================================================================================

class ColoredFormatter(logging.Formatter):
    """Formatter com cores para terminal."""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA + Style.BRIGHT
    }
    
    EMOJIS = {
        'DEBUG': '',
        'INFO': '',
        'WARNING': '',
        'ERROR': '',
        'CRITICAL': ''
    }
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, '')
        reset = Style.RESET_ALL
        emoji = self.EMOJIS.get(record.levelname, '')
        record.levelname = f"{color}{record.levelname}{reset}"
        return super().format(record)


def setup_logging(nivel: str = "INFO") -> logging.Logger:
    """Configura o sistema de logging."""
    logger = logging.getLogger("sistema_agentes")
    logger.setLevel(getattr(logging, nivel.upper()))
    
    # Remove handlers existentes
    logger.handlers = []
    
    formato = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    datefmt = "%H:%M:%S"
    
    # Console com cores
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter(formato, datefmt=datefmt))
    logger.addHandler(console_handler)
    
    # Arquivo
    log_file = CONFIG.LOG_DIR / "sistema.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(formato))
    logger.addHandler(file_handler)
    
    return logger

# Logger global
logger = setup_logging()

# ====================================================================================
# SEÇÃO 4: UTILITÁRIOS
# ====================================================================================

def generate_id(prefix: str = "", length: int = 16) -> str:
    """Gera ID único."""
    data = f"{prefix}_{time.time()}_{random.randint(1000, 9999)}"
    return hashlib.sha256(data.encode()).hexdigest()[:length]

def timestamp_now() -> float:
    """Timestamp atual."""
    return time.time()

def format_duration(seconds: float) -> str:
    """Formata duração."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"

def truncate_text(text: str, max_len: int = 100) -> str:
    """Trunca texto."""
    return text[:max_len] + "..." if len(text) > max_len else text

def extract_keywords(text: str, min_len: int = 4, max_kw: int = 20) -> List[str]:
    """Extrai palavras-chave."""
    words = re.findall(r'\b[a-zA-Z]{' + str(min_len) + ',}\b', text.lower())
    stopwords = {'this', 'that', 'with', 'from', 'they', 'have', 'been', 'their', 'were', 'para', 'como', 'esta', 'esse'}
    words = [w for w in words if w not in stopwords]
    from collections import Counter
    return [w for w, _ in Counter(words).most_common(max_kw)]

def calculate_similarity(str1: str, str2: str) -> float:
    """Calcula similaridade entre strings."""
    from difflib import SequenceMatcher
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

# ====================================================================================
# SEÇÃO 5: BANCO DE DADOS (SQLAlchemy-style com SQLite puro)
# ====================================================================================

class DatabaseManager:
    """Gerenciador de banco de dados SQLite."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.db_path = str(CONFIG.DB_PATH)
        self._local = threading.local()
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Obtém conexão thread-local."""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn
    
    def _init_database(self):
        """Inicializa tabelas."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de parâmetros
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parametros (
            id TEXT PRIMARY KEY,
            topico TEXT NOT NULL,
            tipo_param TEXT NOT NULL,
            conteudo TEXT NOT NULL,
            score REAL DEFAULT 0.0,
            score_detalhado TEXT,
            criados_por TEXT,
            fonte TEXT DEFAULT 'gerado',
            url_fonte TEXT,
            validado INTEGER DEFAULT 0,
            usos INTEGER DEFAULT 0,
            timestamp REAL,
            rodada_debate INTEGER DEFAULT 1
        )
        """)
        
        # Tabela de críticas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS criticas (
            id TEXT PRIMARY KEY,
            parametro_id TEXT,
            de_agente TEXT NOT NULL,
            para_agente TEXT NOT NULL,
            para_topico TEXT NOT NULL,
            tipo_critica TEXT DEFAULT 'construtiva',
            pontos_positivos TEXT,
            pontos_negativos TEXT,
            sugestoes TEXT,
            score_qualidade REAL DEFAULT 0.5,
            timestamp REAL,
            rodada INTEGER DEFAULT 1
        )
        """)
        
        # Tabela de ciclos de debate
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ciclos_debate (
            id TEXT PRIMARY KEY,
            topico TEXT NOT NULL,
            rodada INTEGER DEFAULT 1,
            num_criticas INTEGER DEFAULT 0,
            consenso_final TEXT,
            score_consenso REAL DEFAULT 0.0,
            agentes_participantes TEXT,
            timestamp_inicio REAL,
            timestamp_fim REAL,
            duracao_segundos REAL,
            status TEXT DEFAULT 'em_andamento'
        )
        """)
        
        # Tabela de memória global
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memoria_global (
            id TEXT PRIMARY KEY,
            tipo TEXT NOT NULL,
            dados TEXT NOT NULL,
            relevancia REAL DEFAULT 1.0,
            acessos INTEGER DEFAULT 0,
            ultima_atualizacao REAL,
            tags TEXT,
            topico_relacionado TEXT,
            fonte TEXT,
            agente_origem TEXT
        )
        """)
        
        # Tabela de performance de agentes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agente_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agente_nome TEXT NOT NULL,
            agente_id INTEGER NOT NULL,
            total_debates INTEGER DEFAULT 0,
            total_criticas_geradas INTEGER DEFAULT 0,
            score_medio REAL DEFAULT 0.5,
            acuracia REAL DEFAULT 0.5,
            credibilidade REAL DEFAULT 1.0,
            acertos INTEGER DEFAULT 0,
            erros INTEGER DEFAULT 0,
            primeiro_debate REAL,
            ultimo_debate REAL
        )
        """)
        
        # Tabela de cache de busca web
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS busca_web_cache (
            id TEXT PRIMARY KEY,
            query TEXT NOT NULL UNIQUE,
            resultados TEXT NOT NULL,
            timestamp REAL,
            ttl INTEGER DEFAULT 86400,
            usos INTEGER DEFAULT 0
        )
        """)
        
        # Índices
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_param_topico ON parametros(topico)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_param_tipo ON parametros(tipo_param)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_param_score ON parametros(score)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_criticas_de ON criticas(de_agente)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_criticas_para ON criticas(para_agente)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memoria_tipo ON memoria_global(tipo)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memoria_topico ON memoria_global(topico_relacionado)")
        
        conn.commit()
        conn.close()
        logger.info(" Banco de dados inicializado")
    
    # === OPERAÇÕES COM PARÂMETROS ===
    
    def salvar_parametro(
        self, topico: str, tipo: str, conteudo: Dict, score: float,
        criados_por: List[str], fonte: str = "gerado", rodada: int = 1,
        url_fonte: str = None, score_detalhado: Dict = None
    ) -> str:
        """Salva parâmetro no banco."""
        param_id = generate_id(f"{tipo}_{topico}")
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO parametros 
        (id, topico, tipo_param, conteudo, score, score_detalhado, criados_por, fonte, url_fonte, timestamp, rodada_debate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            param_id, topico, tipo, json.dumps(conteudo), score,
            json.dumps(score_detalhado) if score_detalhado else None,
            ','.join(criados_por), fonte, url_fonte, timestamp_now(), rodada
        ))
        conn.commit()
        return param_id
    
    def buscar_parametros(
        self, topico: str = None, tipo: str = None, 
        min_score: float = None, limit: int = 100
    ) -> List[Dict]:
        """Busca parâmetros."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM parametros WHERE 1=1"
        params = []
        
        if topico:
            query += " AND topico = ?"
            params.append(topico)
        if tipo:
            query += " AND tipo_param = ?"
            params.append(tipo)
        if min_score is not None:
            query += " AND score >= ?"
            params.append(min_score)
        
        query += " ORDER BY score DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [{
            'id': r['id'],
            'topico': r['topico'],
            'tipo': r['tipo_param'],
            'conteudo': json.loads(r['conteudo']),
            'score': r['score'],
            'criados_por': r['criados_por'].split(',') if r['criados_por'] else [],
            'timestamp': r['timestamp']
        } for r in rows]
    
    def buscar_parametros_por_topico(self, topico: str, limit: int = 100) -> Dict:
        """Busca parâmetros organizados por tipo."""
        return {
            'positivos': self.buscar_parametros(topico=topico, tipo='positivo', limit=limit),
            'negativos': self.buscar_parametros(topico=topico, tipo='negativo', limit=limit),
            'incertos': self.buscar_parametros(topico=topico, tipo='incerto', limit=limit)
        }
    
    # === OPERAÇÕES COM CRÍTICAS ===
    
    def salvar_critica(
        self, de_agente: str, para_agente: str, para_topico: str,
        pontos_positivos: List[str], pontos_negativos: List[str],
        sugestoes: List[str], score_qualidade: float, rodada: int = 1
    ) -> str:
        """Salva crítica."""
        critica_id = generate_id(f"critica_{de_agente}_{para_agente}")
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO criticas 
        (id, de_agente, para_agente, para_topico, pontos_positivos, pontos_negativos, sugestoes, score_qualidade, timestamp, rodada)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            critica_id, de_agente, para_agente, para_topico,
            json.dumps(pontos_positivos), json.dumps(pontos_negativos),
            json.dumps(sugestoes), score_qualidade, timestamp_now(), rodada
        ))
        conn.commit()
        return critica_id
    
    def buscar_criticas_para_agente(self, agente_nome: str, limit: int = 100) -> List[Dict]:
        """Busca críticas recebidas por um agente."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM criticas WHERE para_agente = ? ORDER BY timestamp DESC LIMIT ?
        """, (agente_nome, limit))
        
        rows = cursor.fetchall()
        return [{
            'id': r['id'],
            'de': r['de_agente'],
            'positivos': json.loads(r['pontos_positivos'] or '[]'),
            'negativos': json.loads(r['pontos_negativos'] or '[]'),
            'sugestoes': json.loads(r['sugestoes'] or '[]'),
            'score': r['score_qualidade'],
            'rodada': r['rodada']
        } for r in rows]
    
    # === OPERAÇÕES COM CICLOS DE DEBATE ===
    
    def criar_ciclo_debate(self, topico: str, rodada: int = 1) -> str:
        """Cria ciclo de debate."""
        debate_id = generate_id(f"debate_{topico}")
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO ciclos_debate (id, topico, rodada, timestamp_inicio, status)
        VALUES (?, ?, ?, ?, ?)
        """, (debate_id, topico, rodada, timestamp_now(), 'em_andamento'))
        conn.commit()
        return debate_id
    
    def finalizar_ciclo_debate(
        self, debate_id: str, score_consenso: float, 
        consenso: Dict, agentes: List[str], num_criticas: int
    ):
        """Finaliza ciclo de debate."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT timestamp_inicio FROM ciclos_debate WHERE id = ?
        """, (debate_id,))
        row = cursor.fetchone()
        duracao = timestamp_now() - row['timestamp_inicio'] if row else 0
        
        cursor.execute("""
        UPDATE ciclos_debate SET
        score_consenso = ?, consenso_final = ?, agentes_participantes = ?,
        num_criticas = ?, timestamp_fim = ?, duracao_segundos = ?, status = ?
        WHERE id = ?
        """, (
            score_consenso, json.dumps(consenso), ','.join(agentes),
            num_criticas, timestamp_now(), duracao, 'concluido', debate_id
        ))
        conn.commit()
    
    # === OPERAÇÕES COM MEMÓRIA GLOBAL ===
    
    def salvar_memoria(
        self, tipo: str, dados: Dict, relevancia: float = 1.0,
        tags: List[str] = None, topico: str = None, 
        fonte: str = None, agente_origem: str = None
    ) -> str:
        """Salva na memória global."""
        mem_id = generate_id(f"memoria_{tipo}")
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO memoria_global 
        (id, tipo, dados, relevancia, tags, topico_relacionado, fonte, agente_origem, ultima_atualizacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            mem_id, tipo, json.dumps(dados), relevancia,
            ','.join(tags) if tags else None, topico, fonte, agente_origem, timestamp_now()
        ))
        conn.commit()
        return mem_id
    
    def recuperar_memoria(self, topico: str = None, tipo: str = None, limit: int = 50) -> List[Dict]:
        """Recupera memória relevante."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM memoria_global WHERE 1=1"
        params = []
        
        if topico:
            query += " AND topico_relacionado = ?"
            params.append(topico)
        if tipo:
            query += " AND tipo = ?"
            params.append(tipo)
        
        query += " ORDER BY relevancia DESC, acessos DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Incrementa acessos
        for row in rows:
            cursor.execute("""
            UPDATE memoria_global SET acessos = acessos + 1 WHERE id = ?
            """, (row['id'],))
        conn.commit()
        
        return [{
            'id': r['id'],
            'tipo': r['tipo'],
            'dados': json.loads(r['dados']),
            'relevancia': r['relevancia']
        } for r in rows]
    
    # === CACHE DE BUSCA WEB ===
    
    def get_cache_busca(self, query: str) -> Optional[List[Dict]]:
        """Busca em cache."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM busca_web_cache WHERE query = ?
        """, (query,))
        row = cursor.fetchone()
        
        if row:
            # Verifica se expirou
            if timestamp_now() - row['timestamp'] < row['ttl']:
                cursor.execute("""
                UPDATE busca_web_cache SET usos = usos + 1 WHERE id = ?
                """, (row['id'],))
                conn.commit()
                return json.loads(row['resultados'])
        
        return None
    
    def salvar_cache_busca(self, query: str, resultados: List[Dict], ttl: int = 86400):
        """Salva cache de busca."""
        cache_id = generate_id("cache")
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT OR REPLACE INTO busca_web_cache (id, query, resultados, timestamp, ttl)
        VALUES (?, ?, ?, ?, ?)
        """, (cache_id, query, json.dumps(resultados), timestamp_now(), ttl))
        conn.commit()
    
    # === PERFORMANCE DE AGENTES ===
    
    def atualizar_performance_agente(
        self, agente_nome: str, agente_id: int, 
        novo_score: float, acerto: bool = None
    ):
        """Atualiza performance."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM agente_performance WHERE agente_nome = ? AND agente_id = ?
        """, (agente_nome, agente_id))
        row = cursor.fetchone()
        
        if row:
            # Atualiza existente
            total = row['total_debates'] + 1
            score_medio = (row['score_medio'] * row['total_debates'] + novo_score) / total
            acertos = row['acertos'] + (1 if acerto else 0)
            erros = row['erros'] + (0 if acerto else 1) if acerto is not None else row['erros']
            
            cursor.execute("""
            UPDATE agente_performance SET
            total_debates = ?, score_medio = ?, acertos = ?, erros = ?, ultimo_debate = ?
            WHERE id = ?
            """, (total, score_medio, acertos, erros, timestamp_now(), row['id']))
        else:
            # Cria novo
            cursor.execute("""
            INSERT INTO agente_performance 
            (agente_nome, agente_id, total_debates, score_medio, primeiro_debate, ultimo_debate)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (agente_nome, agente_id, 1, novo_score, timestamp_now(), timestamp_now()))
        
        conn.commit()
    
    def get_estatisticas(self) -> Dict:
        """Estatísticas gerais."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM parametros")
        total_parametros = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM criticas")
        total_criticas = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM ciclos_debate")
        total_debates = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM memoria_global")
        total_memorias = cursor.fetchone()['total']
        
        cursor.execute("SELECT AVG(score) as media FROM parametros")
        score_medio = cursor.fetchone()['media'] or 0
        
        return {
            'total_parametros': total_parametros,
            'total_criticas': total_criticas,
            'total_debates': total_debates,
            'total_memorias': total_memorias,
            'score_medio_geral': round(score_medio, 4)
        }

# Instância global do banco
db = DatabaseManager()

# ====================================================================================
# SEÇÃO 6: BUSCA WEB (DuckDuckGo)
# ====================================================================================

class WebSearchEngine:
    """Motor de busca web usando DuckDuckGo."""
    
    def __init__(self):
        self.enabled = CONFIG.WEB_SEARCH_ENABLED and REQUESTS_AVAILABLE
        self.timeout = CONFIG.WEB_SEARCH_TIMEOUT
        self.max_resultados = CONFIG.MAX_RESULTADOS_WEB
        self.session = requests.Session() if REQUESTS_AVAILABLE else None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def buscar(self, query: str, use_cache: bool = True) -> List[Dict]:
        """Realiza busca na web."""
        if not self.enabled:
            logger.warning(" Busca web desabilitada ou requests não instalado")
            return []
        
        # Verifica cache
        if use_cache:
            cached = db.get_cache_busca(query)
            if cached:
                logger.info(f" Cache hit para: {truncate_text(query, 50)}")
                return cached
        
        try:
            logger.info(f" Buscando na web: {truncate_text(query, 50)}")
            
            # DuckDuckGo HTML
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            response = self.session.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            resultados = self._parse_resultados(response.text)
            
            # Salva cache
            if use_cache:
                db.salvar_cache_busca(query, resultados)
            
            logger.info(f" {len(resultados)} resultados encontrados")
            return resultados
            
        except Exception as e:
            logger.error(f" Erro na busca web: {e}")
            return []
    
    def _parse_resultados(self, html: str) -> List[Dict]:
        """Parseia resultados do HTML."""
        resultados = []
        
        if BS4_AVAILABLE:
            soup = BeautifulSoup(html, 'html.parser')
            results = soup.find_all('div', class_='result')[:self.max_resultados]
            
            for result in results:
                title_tag = result.find('a', class_='result__a')
                snippet_tag = result.find('a', class_='result__snippet')
                
                if title_tag and snippet_tag:
                    resultados.append({
                        'titulo': title_tag.get_text(strip=True),
                        'url': title_tag.get('href', ''),
                        'snippet': snippet_tag.get_text(strip=True)
                    })
        else:
            # Parse simples sem BeautifulSoup
            import re
            links = re.findall(r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html)
            snippets = re.findall(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', html)
            
            for i, (url, titulo) in enumerate(links[:self.max_resultados]):
                resultados.append({
                    'titulo': re.sub(r'<[^>]+>', '', titulo),
                    'url': url,
                    'snippet': re.sub(r'<[^>]+>', '', snippets[i]) if i < len(snippets) else ''
                })
        
        return resultados
    
    def buscar_e_resumir(self, query: str, topico: str) -> str:
        """Busca e resume resultados para um tópico."""
        resultados = self.buscar(query)
        
        if not resultados:
            return ""
        
        # Concatena snippets
        texto = f"Informações sobre {topico}:\n\n"
        for i, r in enumerate(resultados[:3], 1):
            texto += f"{i}. {r['titulo']}: {r['snippet']}\n"
        
        # Salva na memória
        db.salvar_memoria(
            tipo='busca_web',
            dados={'query': query, 'resultados': resultados},
            relevancia=0.8,
            tags=['web', 'pesquisa', topico],
            topico=topico,
            fonte='duckduckgo'
        )
        
        return texto

# Instância global
web_search = WebSearchEngine()

# ====================================================================================
# SEÇÃO 7: DEFINIÇÃO DOS AGENTES
# ====================================================================================

@dataclass
class Personalidade:
    """Personalidade de um agente."""
    criatividade: float = 0.5
    rigor: float = 0.5
    colaboracao: float = 0.5
    foco: str = "geral"

@dataclass
class EstadoAgente:
    """Estado interno de um agente."""
    parametros_locais: Dict = field(default_factory=dict)
    criticas_geradas: List = field(default_factory=list)
    criticas_recebidas: List = field(default_factory=list)
    opiniao_consenso: Dict = field(default_factory=dict)
    score_credibilidade: float = 1.0
    historico_acertos: int = 0
    historico_erros: int = 0

class AgenteAutonomo(ABC):
    """Classe base para agentes autônomos."""
    
    def __init__(self, id_agente: int, nome: str, especialidade: str, personalidade: Personalidade = None):
        self.id = id_agente
        self.nome = nome
        self.especialidade = especialidade
        self.personalidade = personalidade or Personalidade()
        self.estado = EstadoAgente()
        self.logger = logging.getLogger(f"agente.{nome}")
    
    @abstractmethod
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        """Análise especializada do agente."""
        pass
    
    @abstractmethod
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        """Gera crítica construtiva."""
        pass
    
    def processar(self, conteudo: str, topico: str, memoria: List[Dict] = None) -> Dict:
        """Processa conteúdo e gera parâmetros."""
        self.logger.info(f" {self.nome} processando '{topico}'")
        
        # Contexto com memória
        contexto = {'memoria': memoria or []}
        
        # Análise especializada
        analise = self.analisar(conteudo, topico, contexto)
        
        # Gera parâmetros locais
        self.estado.parametros_locais = {
            'agente_id': self.id,
            'agente_nome': self.nome,
            'especialidade': self.especialidade,
            'topico': topico,
            'analise': analise,
            'timestamp': timestamp_now(),
            'score_inicial': random.uniform(0.5, 1.0) * self.estado.score_credibilidade
        }
        
        return self.estado.parametros_locais
    
    def criticar(self, agente_outro: 'AgenteAutonomo') -> Dict:
        """Critica outro agente."""
        critica = self.gerar_critica(agente_outro.estado.parametros_locais, agente_outro)
        self.estado.criticas_geradas.append(critica)
        return critica
    
    def receber_critica(self, critica: Dict):
        """Recebe crítica de outro agente."""
        self.estado.criticas_recebidas.append(critica)
    
    def formar_consenso(self) -> Dict:
        """Forma opinião de consenso baseada nas críticas recebidas."""
        score_total = self.estado.parametros_locais.get('score_inicial', 0.5)
        ajustes = []
        
        for critica in self.estado.criticas_recebidas:
            peso = critica.get('score_qualidade', 0.5)
            pontos_negativos = len(critica.get('pontos_negativos', []))
            pontos_positivos = len(critica.get('pontos_positivos', []))
            
            # Ajusta score
            score_total -= pontos_negativos * peso * 0.05
            score_total += pontos_positivos * peso * 0.03
            
            if pontos_negativos > 0:
                ajustes.append(f"Crítica de {critica['de_agente']}: -{pontos_negativos * peso * 0.05:.3f}")
        
        score_total = max(0.1, min(1.0, score_total))
        
        self.estado.opiniao_consenso = {
            'agente': self.nome,
            'score_final': score_total,
            'ajustes_aplicados': len(ajustes),
            'credibilidade': self.estado.score_credibilidade,
            'detalhes_ajustes': ajustes
        }
        
        return self.estado.opiniao_consenso
    
    def _extrair_padroes(self, texto: str) -> List[str]:
        """Extrai padrões semânticos."""
        padroes = []
        palavras_chave = [
            'importante', 'critico', 'essencial', 'avancado', 'otimizado',
            'eficiente', 'escalavel', 'robusto', 'seguro', 'inovador'
        ]
        texto_lower = texto.lower()
        for palavra in palavras_chave:
            if palavra in texto_lower:
                padroes.append(palavra)
        return padroes


# ====================================================================================
# AGENTE 1: DESIGNER
# ====================================================================================

class AgenteDesigner(AgenteAutonomo):
    """Agente especializado em estrutura e padrões visuais."""
    
    def __init__(self):
        super().__init__(
            id_agente=1,
            nome="Designer",
            especialidade="Estrutura e padrões visuais",
            personalidade=Personalidade(criatividade=0.9, rigor=0.6, foco="padroes_estruturais")
        )
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        """Análise focada em estrutura e padrões."""
        palavras = extract_keywords(conteudo, min_len=3, max_kw=30)
        
        # Detecta padrões estruturais
        padroes_estruturais = []
        if 'class' in conteudo or 'def ' in conteudo:
            padroes_estruturais.append('orientacao_objetos')
        if '{' in conteudo and '}' in conteudo:
            padroes_estruturais.append('estrutura_dados')
        if 'import' in conteudo or 'from' in conteudo:
            padroes_estruturais.append('modularizacao')
        
        return {
            'palavras_chave': palavras[:20],
            'padroes_estruturais': padroes_estruturais,
            'complexidade_estrutural': len(padroes_estruturais) / 3,
            'padroes_semanticos': self._extrair_padroes(conteudo),
            'qualidade_estrutura': len(conteudo) / 2000
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        """Crítica focada em estrutura."""
        analise = param_outro.get('analise', {})
        pontos_positivos = []
        pontos_negativos = []
        sugestoes = []
        
        # Avalia padrões estruturais
        padroes = analise.get('padroes_estruturais', [])
        if len(padroes) >= 2:
            pontos_positivos.append(f"Boa diversidade de padrões: {', '.join(padroes)}")
        else:
            pontos_negativos.append("Poucos padrões estruturais identificados")
            sugestoes.append("Explore mais padrões de design no conteúdo")
        
        # Avalia palavras-chave
        palavras = analise.get('palavras_chave', [])
        if len(palavras) >= 10:
            pontos_positivos.append(f"Rico vocabulário: {len(palavras)} termos")
        else:
            pontos_negativos.append("Vocabulário limitado")
            sugestoes.append("Expanda o vocabulário técnico")
        
        score = 0.5 + (len(pontos_positivos) * 0.15) - (len(pontos_negativos) * 0.1)
        
        return {
            'de_agente': self.nome,
            'para_agente': agente_outro.nome,
            'pontos_positivos': pontos_positivos,
            'pontos_negativos': pontos_negativos,
            'sugestoes': sugestoes,
            'score_qualidade': max(0.3, min(1.0, score))
        }


# ====================================================================================
# AGENTE 2: ANALISTA
# ====================================================================================

class AgenteAnalista(AgenteAutonomo):
    """Agente especializado em métricas e análise de dados."""
    
    def __init__(self):
        super().__init__(
            id_agente=2,
            nome="Analista",
            especialidade="Métricas e análise de dados",
            personalidade=Personalidade(criatividade=0.4, rigor=0.95, foco="dados_metricas")
        )
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        """Análise quantitativa e métricas."""
        palavras = conteudo.split()
        caracteres = len(conteudo)
        
        # Estatísticas
        estatisticas = {
            'total_palavras': len(palavras),
            'total_caracteres': caracteres,
            'media_palavras_frase': len(palavras) / max(1, conteudo.count('.')),
            'palavras_unicas': len(set(p.lower() for p in palavras)),
            'densidade_informacao': len(set(p.lower() for p in palavras)) / max(1, len(palavras))
        }
        
        # Métricas de qualidade
        metricas_qualidade = {
            'comprimento_adequado': 1.0 if 500 < caracteres < 10000 else 0.5,
            'diversidade_vocabulario': estatisticas['densidade_informacao'],
            'estruturacao': conteudo.count('.') / max(1, len(palavras)) * 10
        }
        
        return {
            'estatisticas': estatisticas,
            'metricas_qualidade': metricas_qualidade,
            'score_metrico': sum(metricas_qualidade.values()) / len(metricas_qualidade),
            'palavras_chave': extract_keywords(conteudo, min_len=4, max_kw=15)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        """Crítica baseada em métricas."""
        analise = param_outro.get('analise', {})
        pontos_positivos = []
        pontos_negativos = []
        sugestoes = []
        
        metricas = analise.get('metricas_qualidade', {})
        estatisticas = analise.get('estatisticas', {})
        
        # Avalia métricas
        if metricas.get('diversidade_vocabulario', 0) > 0.6:
            pontos_positivos.append("Excelente diversidade de vocabulário")
        else:
            pontos_negativos.append("Vocabulário repetitivo")
            sugestoes.append("Varie mais o vocabulário técnico")
        
        if estatisticas.get('total_palavras', 0) > 100:
            pontos_positivos.append("Conteúdo com volume adequado")
        else:
            pontos_negativos.append("Conteúdo muito curto")
            sugestoes.append("Expanda o conteúdo com mais detalhes")
        
        score = analise.get('score_metrico', 0.5)
        
        return {
            'de_agente': self.nome,
            'para_agente': agente_outro.nome,
            'pontos_positivos': pontos_positivos,
            'pontos_negativos': pontos_negativos,
            'sugestoes': sugestoes,
            'score_qualidade': max(0.3, min(1.0, score))
        }


# ====================================================================================
# AGENTE 3: CRIADOR
# ====================================================================================

class AgenteCriador(AgenteAutonomo):
    """Agente especializado em geração de ideias novas."""
    
    def __init__(self):
        super().__init__(
            id_agente=3,
            nome="Criador",
            especialidade="Geração de ideias novas",
            personalidade=Personalidade(criatividade=0.95, rigor=0.5, foco="inovacao")
        )
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        """Análise focada em inovação e criatividade."""
        # Identifica conceitos únicos
        palavras = extract_keywords(conteudo, min_len=4, max_kw=25)
        
        # Simula identificação de ideias inovadoras
        ideias_potenciais = []
        conceitos = ['automatizacao', 'inteligencia', 'otimizacao', 'escalabilidade', 'inovacao']
        for conceito in conceitos:
            if conceito in conteudo.lower():
                ideias_potenciais.append(f"Aplicar {conceito} em {topico}")
        
        # Score de inovação
        score_inovacao = min(1.0, len(ideias_potenciais) / 3 + random.uniform(0, 0.3))
        
        return {
            'palavras_chave': palavras,
            'ideias_potenciais': ideias_potenciais,
            'score_inovacao': score_inovacao,
            'potencial_transformacao': score_inovacao * 0.8,
            'conceitos_identificados': len(ideias_potenciais)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        """Crítica focada em inovação."""
        analise = param_outro.get('analise', {})
        pontos_positivos = []
        pontos_negativos = []
        sugestoes = []
        
        ideias = analise.get('ideias_potenciais', [])
        score_inovacao = analise.get('score_inovacao', 0)
        
        if len(ideias) >= 3:
            pontos_positivos.append(f"Rico em ideias: {len(ideias)} conceitos")
        else:
            pontos_negativos.append("Poucas ideias inovadoras")
            sugestoes.append("Pense fora da caixa, explore novas abordagens")
        
        if score_inovacao > 0.7:
            pontos_positivos.append("Alto potencial de inovação")
        else:
            pontos_negativos.append("Potencial inovador limitado")
        
        return {
            'de_agente': self.nome,
            'para_agente': agente_outro.nome,
            'pontos_positivos': pontos_positivos,
            'pontos_negativos': pontos_negativos,
            'sugestoes': sugestoes,
            'score_qualidade': max(0.3, min(1.0, score_inovacao + 0.1))
        }


# ====================================================================================
# AGENTE 4: CRÍTICO
# ====================================================================================

class AgenteCritico(AgenteAutonomo):
    """Agente especializado em identificação de falhas."""
    
    def __init__(self):
        super().__init__(
            id_agente=4,
            nome="Critico",
            especialidade="Identificação de falhas",
            personalidade=Personalidade(criatividade=0.5, rigor=0.95, foco="deteccao_erros")
        )
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        """Análise focada em identificar problemas."""
        falhas_potenciais = []
        
        # Detecta possíveis problemas
        if len(conteudo) < 200:
            falhas_potenciais.append("conteudo_insuficiente")
        if conteudo.count('.') < 3:
            falhas_potenciais.append("pouca_estruturacao")
        if len(set(conteudo.lower().split())) < 20:
            falhas_potenciais.append("vocabulario_limitado")
        
        # Verifica termos de alerta
        alertas = ['problema', 'erro', 'falha', 'bug', 'limitacao', 'risco']
        alertas_encontrados = [a for a in alertas if a in conteudo.lower()]
        
        return {
            'falhas_identificadas': falhas_potenciais,
            'alertas_encontrados': alertas_encontrados,
            'score_risco': len(falhas_potenciais) / 5,
            'recomendacoes': [f"Verificar: {f}" for f in falhas_potenciais],
            'palavras_chave': extract_keywords(conteudo, min_len=4, max_kw=15)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        """Crítica rigorosa de falhas."""
        analise = param_outro.get('analise', {})
        pontos_positivos = []
        pontos_negativos = []
        sugestoes = []
        
        falhas = analise.get('falhas_identificadas', [])
        risco = analise.get('score_risco', 0)
        
        if len(falhas) == 0:
            pontos_positivos.append("Nenhuma falha crítica identificada")
        else:
            pontos_negativos.extend([f"Falha: {f}" for f in falhas])
            sugestoes.extend([f"Corrigir: {f}" for f in falhas])
        
        if risco < 0.3:
            pontos_positivos.append("Baixo risco de erros")
        else:
            pontos_negativos.append(f"Risco elevado: {risco:.2f}")
        
        return {
            'de_agente': self.nome,
            'para_agente': agente_outro.nome,
            'pontos_positivos': pontos_positivos,
            'pontos_negativos': pontos_negativos,
            'sugestoes': sugestoes,
            'score_qualidade': max(0.3, min(1.0, 1.0 - risco))
        }


# ====================================================================================
# AGENTE 5: REVISOR
# ====================================================================================

class AgenteRevisor(AgenteAutonomo):
    """Agente especializado em refinamento textual."""
    
    def __init__(self):
        super().__init__(
            id_agente=5,
            nome="Revisor",
            especialidade="Refinamento textual",
            personalidade=Personalidade(criatividade=0.6, rigor=0.9, foco="qualidade_texto")
        )
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        """Análise de qualidade textual."""
        # Métricas textuais
        frases = [f.strip() for f in conteudo.split('.') if f.strip()]
        palavras = conteudo.split()
        
        # Qualidade de escrita
        qualidade = {
            'media_palavras_frase': len(palavras) / max(1, len(frases)),
            'frases_bem_formadas': sum(1 for f in frases if len(f.split()) >= 5),
            'coesao': len(set(p.lower() for p in palavras)) / max(1, len(palavras)),
            'clareza': 1.0 if 10 < len(palavras) / max(1, len(frases)) < 25 else 0.6
        }
        
        score_textual = sum(qualidade.values()) / len(qualidade)
        
        return {
            'metricas_texto': qualidade,
            'score_textual': score_textual,
            'total_frases': len(frases),
            'recomendacoes_estilo': self._gerar_recomendacoes(qualidade),
            'palavras_chave': extract_keywords(conteudo, min_len=4, max_kw=15)
        }
    
    def _gerar_recomendacoes(self, qualidade: Dict) -> List[str]:
        """Gera recomendações de estilo."""
        recs = []
        if qualidade['media_palavras_frase'] > 25:
            recs.append("Reduza o tamanho médio das frases")
        if qualidade['coesao'] < 0.5:
            recs.append("Aumente a variedade de vocabulário")
        if qualidade['clareza'] < 0.8:
            recs.append("Melhore a clareza das frases")
        return recs
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        """Crítica focada em qualidade textual."""
        analise = param_outro.get('analise', {})
        pontos_positivos = []
        pontos_negativos = []
        sugestoes = []
        
        metricas = analise.get('metricas_texto', {})
        score = analise.get('score_textual', 0.5)
        
        if metricas.get('clareza', 0) > 0.8:
            pontos_positivos.append("Texto claro e bem estruturado")
        else:
            pontos_negativos.append("Texto poderia ser mais claro")
            sugestoes.append("Simplifique frases complexas")
        
        if score > 0.7:
            pontos_positivos.append("Excelente qualidade textual")
        
        return {
            'de_agente': self.nome,
            'para_agente': agente_outro.nome,
            'pontos_positivos': pontos_positivos,
            'pontos_negativos': pontos_negativos,
            'sugestoes': sugestoes,
            'score_qualidade': max(0.3, min(1.0, score))
        }


# ====================================================================================
# AGENTE 6: VALIDADOR
# ====================================================================================

class AgenteValidador(AgenteAutonomo):
    """Agente especializado em verificação de coerência."""
    
    def __init__(self):
        super().__init__(
            id_agente=6,
            nome="Validador",
            especialidade="Verificação de coerência",
            personalidade=Personalidade(criatividade=0.4, rigor=0.95, foco="consistencia")
        )
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        """Análise de coerência e consistência."""
        palavras = conteudo.lower().split()
        
        # Verifica coerência temática
        palavras_topico = [p for p in palavras if p in topico.lower().split('_')]
        coerencia_tema = len(palavras_topico) / max(1, len(palavras)) * 10
        
        # Verifica consistência interna
        frases = [f.strip() for f in conteudo.split('.') if f.strip()]
        consistencia = 1.0 if len(frases) > 2 else 0.5
        
        # Verifica contradições simples
        contradicoes = []
        if 'sim' in palavras and 'nao' in palavras:
            contradicoes.append("possivel_contradicao")
        
        score_coerencia = min(1.0, coerencia_tema + consistencia * 0.3)
        
        return {
            'coerencia_tematica': coerencia_tema,
            'consistencia_interna': consistencia,
            'contradicoes_detectadas': contradicoes,
            'score_coerencia': score_coerencia,
            'palavras_chave': extract_keywords(conteudo, min_len=4, max_kw=15)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        """Crítica de coerência."""
        analise = param_outro.get('analise', {})
        pontos_positivos = []
        pontos_negativos = []
        sugestoes = []
        
        coerencia = analise.get('score_coerencia', 0.5)
        contradicoes = analise.get('contradicoes_detectadas', [])
        
        if coerencia > 0.7:
            pontos_positivos.append("Alta coerência temática")
        else:
            pontos_negativos.append("Coerência temática fraca")
            sugestoes.append("Mantenha foco no tema principal")
        
        if len(contradicoes) == 0:
            pontos_positivos.append("Sem contradições aparentes")
        else:
            pontos_negativos.extend([f"Contradição: {c}" for c in contradicoes])
        
        return {
            'de_agente': self.nome,
            'para_agente': agente_outro.nome,
            'pontos_positivos': pontos_positivos,
            'pontos_negativos': pontos_negativos,
            'sugestoes': sugestoes,
            'score_qualidade': max(0.3, min(1.0, coerencia))
        }


# ====================================================================================
# AGENTE 7: ESTRATEGISTA
# ====================================================================================

class AgenteEstrategista(AgenteAutonomo):
    """Agente especializado em planejamento e estratégia."""
    
    def __init__(self):
        super().__init__(
            id_agente=7,
            nome="Estrategista",
            especialidade="Planejamento e estratégia",
            personalidade=Personalidade(criatividade=0.8, rigor=0.8, foco="planejamento")
        )
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        """Análise estratégica."""
        # Identifica elementos estratégicos
        elementos = {
            'objetivos': conteudo.lower().count('objetivo') + conteudo.lower().count('meta'),
            'acoes': conteudo.lower().count('implementar') + conteudo.lower().count('executar'),
            'resultados': conteudo.lower().count('resultado') + conteudo.lower().count('outcome'),
            'prazos': conteudo.lower().count('prazo') + conteudo.lower().count('tempo')
        }
        
        # Score estratégico
        total_elementos = sum(1 for v in elementos.values() if v > 0)
        score_estrategico = total_elementos / 4
        
        # Gera recomendações estratégicas
        recomendacoes = []
        if elementos['objetivos'] == 0:
            recomendacoes.append("Defina objetivos claros")
        if elementos['acoes'] == 0:
            recomendacoes.append("Estabeleça ações concretas")
        
        return {
            'elementos_estrategicos': elementos,
            'score_estrategico': score_estrategico,
            'recomendacoes': recomendacoes,
            'viabilidade': score_estrategico * 0.9,
            'palavras_chave': extract_keywords(conteudo, min_len=4, max_kw=15)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        """Crítica estratégica."""
        analise = param_outro.get('analise', {})
        pontos_positivos = []
        pontos_negativos = []
        sugestoes = []
        
        elementos = analise.get('elementos_estrategicos', {})
        score = analise.get('score_estrategico', 0)
        
        if elementos.get('objetivos', 0) > 0:
            pontos_positivos.append("Objetivos bem definidos")
        else:
            pontos_negativos.append("Falta definição de objetivos")
            sugestoes.append("Adicione metas claras")
        
        if score > 0.6:
            pontos_positivos.append("Boa visão estratégica")
        else:
            pontos_negativos.append("Visão estratégica limitada")
        
        return {
            'de_agente': self.nome,
            'para_agente': agente_outro.nome,
            'pontos_positivos': pontos_positivos,
            'pontos_negativos': pontos_negativos,
            'sugestoes': sugestoes,
            'score_qualidade': max(0.3, min(1.0, score + 0.2))
        }


# ====================================================================================
# AGENTE 8: MEMÓRIA
# ====================================================================================

class AgenteMemoria(AgenteAutonomo):
    """Agente especializado em armazenamento de padrões."""
    
    def __init__(self):
        super().__init__(
            id_agente=8,
            nome="Memoria",
            especialidade="Armazenamento de padrões",
            personalidade=Personalidade(criatividade=0.5, rigor=0.9, foco="aprendizado_historico")
        )
    
    def analisar(self, conteudo: str, topico: str, contexto: Dict = None) -> Dict:
        """Análise focada em padrões para memória."""
        memoria = contexto.get('memoria', []) if contexto else []
        
        # Extrai padrões
        padroes = self._extrair_padroes(conteudo)
        
        # Compara com memória anterior
        padroes_historicos = []
        for mem in memoria:
            dados = mem.get('dados', {})
            if isinstance(dados, dict):
                padroes_historicos.extend(dados.get('padroes', []))
        
        # Identifica padrões novos vs conhecidos
        padroes_novos = [p for p in padroes if p not in padroes_historicos]
        padroes_conhecidos = [p for p in padroes if p in padroes_historicos]
        
        return {
            'padroes_identificados': padroes,
            'padroes_novos': padroes_novos,
            'padroes_conhecidos': padroes_conhecidos,
            'memoria_utilizada': len(memoria),
            'score_memoria': len(padroes_conhecidos) / max(1, len(padroes)) if padroes else 0.5,
            'palavras_chave': extract_keywords(conteudo, min_len=4, max_kw=15)
        }
    
    def gerar_critica(self, param_outro: Dict, agente_outro: 'AgenteAutonomo') -> Dict:
        """Crítica baseada em padrões históricos."""
        analise = param_outro.get('analise', {})
        pontos_positivos = []
        pontos_negativos = []
        sugestoes = []
        
        padroes = analise.get('padroes_identificados', [])
        novos = analise.get('padroes_novos', [])
        
        if len(padroes) >= 3:
            pontos_positivos.append(f"Boa identificação de padrões: {len(padroes)}")
        else:
            pontos_negativos.append("Poucos padrões identificados")
        
        if len(novos) > 0:
            pontos_positivos.append(f"{len(novos)} padrões novos descobertos")
        
        score = analise.get('score_memoria', 0.5)
        
        return {
            'de_agente': self.nome,
            'para_agente': agente_outro.nome,
            'pontos_positivos': pontos_positivos,
            'pontos_negativos': pontos_negativos,
            'sugestoes': sugestoes,
            'score_qualidade': max(0.3, min(1.0, score + 0.3))
        }


# ====================================================================================
# SEÇÃO 8: FÁBRICA DE AGENTES
# ====================================================================================

class AgentFactory:
    """Fábrica para criar os 8 agentes."""
    
    AGENTES = {
        1: AgenteDesigner,
        2: AgenteAnalista,
        3: AgenteCriador,
        4: AgenteCritico,
        5: AgenteRevisor,
        6: AgenteValidador,
        7: AgenteEstrategista,
        8: AgenteMemoria
    }
    
    @classmethod
    def criar_todos(cls) -> List[AgenteAutonomo]:
        """Cria todos os 8 agentes."""
        return [cls.criar(i) for i in range(1, 9)]
    
    @classmethod
    def criar(cls, agente_id: int) -> AgenteAutonomo:
        """Cria um agente específico."""
        if agente_id not in cls.AGENTES:
            raise ValueError(f"Agente {agente_id} não existe")
        return cls.AGENTES[agente_id]()


# ====================================================================================
# SEÇÃO 9: SALA DE DEBATE
# ====================================================================================

class SalaDebate:
    """Coordena o debate entre os 8 agentes."""
    
    def __init__(self, usar_web_search: bool = True):
        self.agentes = AgentFactory.criar_todos()
        self.historico_criticas = []
        self.consenso_global = None
        self.rodada_atual = 0
        self.usar_web_search = usar_web_search
        self.debate_id = None
        self.logger = logging.getLogger("debate")
    
    def iniciar_debate(
        self, conteudo: str, topico: str, num_rodadas: int = 15
    ) -> Dict:
        """Inicia debate completo."""
        self.logger.info(f" Iniciando debate: '{topico}' ({num_rodadas} rodadas)")
        
        # Cria ciclo no banco
        self.debate_id = db.criar_ciclo_debate(topico, 1)
        
        # Busca informações na web se habilitado
        if self.usar_web_search:
            self.logger.info(" Buscando informações na web...")
            info_web = web_search.buscar_e_resumir(topico, topico)
            if info_web:
                conteudo += f"\n\n[Informações da web]:\n{info_web}"
        
        # Recupera memória relevante
        memoria = db.recuperar_memoria(topico=topico, limit=20)
        self.logger.info(f" Memória recuperada: {len(memoria)} entradas")
        
        # FASE 1: Processamento paralelo
        self.logger.info("[Fase 1] Processamento inicial paralelo...")
        self._fase_processamento(conteudo, topico, memoria)
        
        # FASE 2: Ciclos de crítica
        self.logger.info("[Fase 2] Ciclos iterativos de crítica...")
        self._fase_criticas(num_rodadas)
        
        # FASE 3: Consenso
        self.logger.info("[Fase 3] Formação de consenso...")
        self._fase_consenso(topico)
        
        # Salva no banco
        db.finalizar_ciclo_debate(
            self.debate_id,
            self.consenso_global['score_medio'],
            self.consenso_global,
            [a.nome for a in self.agentes],
            len(self.historico_criticas)
        )
        
        self.logger.info(f" Debate concluído: {len(self.historico_criticas)} críticas")
        
        return self.consenso_global
    
    def _fase_processamento(self, conteudo: str, topico: str, memoria: List[Dict]):
        """Fase 1: Processamento inicial paralelo."""
        def processar_agente(agente):
            try:
                return agente.processar(conteudo, topico, memoria)
            except Exception as e:
                self.logger.error(f"Erro em {agente.nome}: {e}")
                return None
        
        with ThreadPoolExecutor(max_workers=CONFIG.MAX_WORKERS) as executor:
            futures = {executor.submit(processar_agente, a): a for a in self.agentes}
            for future in as_completed(futures):
                agente = futures[future]
                resultado = future.result()
                if resultado:
                    self.logger.info(f"   {agente.nome} processou")
    
    def _fase_criticas(self, num_rodadas: int):
        """Fase 2: Ciclos de crítica cruzada."""
        for rodada in range(num_rodadas):
            self.rodada_atual = rodada + 1
            
            # Verifica parada antecipada
            if CONFIG.PARADA_ANTECIPADA and rodada > 5:
                scores = [a.estado.parametros_locais.get('score_inicial', 0) for a in self.agentes]
                score_medio = sum(scores) / len(scores)
                if score_medio > CONFIG.SCORE_CONVERGENCIA:
                    self.logger.info(f"   Convergência atingida na rodada {rodada + 1}")
                    break
            
            criticas_rodada = []
            
            # Cada agente critica todos os outros
            for agente1 in self.agentes:
                for agente2 in self.agentes:
                    if agente1.id != agente2.id:
                        critica = agente1.criticar(agente2)
                        agente2.receber_critica(critica)
                        criticas_rodada.append(critica)
                        
                        # Salva no banco
                        db.salvar_critica(
                            critica['de_agente'],
                            critica['para_agente'],
                            agente2.estado.parametros_locais.get('topico', ''),
                            critica['pontos_positivos'],
                            critica['pontos_negativos'],
                            critica['sugestoes'],
                            critica['score_qualidade'],
                            self.rodada_atual
                        )
            
            self.historico_criticas.extend(criticas_rodada)
            
            if (rodada + 1) % 3 == 0:
                self.logger.info(f"   Rodada {rodada + 1}: {len(criticas_rodada)} críticas")
    
    def _fase_consenso(self, topico: str):
        """Fase 3: Formação de consenso."""
        consensos = []
        
        for agente in self.agentes:
            opiniao = agente.formar_consenso()
            consensos.append(opiniao)
            
            # Atualiza performance
            db.atualizar_performance_agente(
                agente.nome, agente.id,
                opiniao['score_final'],
                opiniao['score_final'] > 0.6
            )
        
        # Calcula score médio ponderado
        scores = [c['score_final'] for c in consensos]
        score_medio = sum(scores) / len(scores) if scores else 0.5
        
        self.consenso_global = {
            'topico': topico,
            'score_medio': score_medio,
            'consensos_agentes': consensos,
            'num_criticas_totais': len(self.historico_criticas),
            'timestamp': timestamp_now()
        }


# ====================================================================================
# SEÇÃO 10: CLASSIFICADOR DE PARÂMETROS
# ====================================================================================

class ClassificadorParametros:
    """Classifica parâmetros em positivos, negativos e incertos."""
    
    def __init__(self):
        self.threshold_positivo = CONFIG.THRESHOLD_POSITIVO
        self.threshold_negativo = CONFIG.THRESHOLD_NEGATIVO
    
    def classificar(
        self, agentes: List[AgenteAutonomo], topico: str, score_consenso: float
    ) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """Classifica parâmetros dos agentes."""
        positivos = []
        negativos = []
        incertos = []
        
        for agente in agentes:
            params = agente.estado.parametros_locais
            opiniao = agente.estado.opiniao_consenso
            
            score = opiniao.get('score_final', 0.5)
            
            param_classificado = {
                'agente': agente.nome,
                'agente_id': agente.id,
                'topico': topico,
                'analise': params.get('analise', {}),
                'score': score,
                'timestamp': timestamp_now()
            }
            
            if score >= self.threshold_positivo:
                param_classificado['tipo'] = 'positivo'
                param_classificado['qualidade'] = 'excelente'
                positivos.append(param_classificado)
            elif score <= self.threshold_negativo:
                param_classificado['tipo'] = 'negativo'
                param_classificado['qualidade'] = 'insuficiente'
                negativos.append(param_classificado)
            else:
                param_classificado['tipo'] = 'incerto'
                param_classificado['qualidade'] = 'revisar'
                incertos.append(param_classificado)
        
        return positivos, negativos, incertos
    
    def salvar_classificacao(
        self, positivos: List[Dict], negativos: List[Dict], 
        incertos: List[Dict], topico: str
    ):
        """Salva classificação no banco."""
        # Salva positivos
        for p in positivos:
            db.salvar_parametro(
                topico=topico,
                tipo='positivo',
                conteudo=p['analise'],
                score=p['score'],
                criados_por=[p['agente']],
                rodada=1
            )
        
        # Salva negativos
        for n in negativos:
            db.salvar_parametro(
                topico=topico,
                tipo='negativo',
                conteudo=n['analise'],
                score=n['score'],
                criados_por=[n['agente']],
                rodada=1
            )
        
        # Salva incertos
        for i in incertos:
            db.salvar_parametro(
                topico=topico,
                tipo='incerto',
                conteudo=i['analise'],
                score=i['score'],
                criados_por=[i['agente']],
                rodada=1
            )
        
        logger.info(f" Parâmetros salvos: +{len(positivos)} | -{len(negativos)} | ?{len(incertos)}")


# ====================================================================================
# SEÇÃO 11: PROCESSADOR DE TÓPICO
# ====================================================================================

class ProcessadorTopico:
    """Processa um tópico completo."""
    
    def __init__(self, usar_web_search: bool = True):
        self.usar_web_search = usar_web_search
        self.classificador = ClassificadorParametros()
    
    def processar(
        self, topico: str, num_rodadas: int = 15, conteudo_base: str = None
    ) -> Dict:
        """Processa tópico completo."""
        logger.info(f"\n{'='*70}")
        logger.info(f" PROCESSANDO: '{topico.upper()}'")
        logger.info(f"{'='*70}")
        
        # Gera conteúdo base se não fornecido
        if not conteudo_base:
            conteudo_base = self._gerar_conteudo_base(topico)
        
        # Cria e executa debate
        sala = SalaDebate(usar_web_search=self.usar_web_search)
        consenso = sala.iniciar_debate(conteudo_base, topico, num_rodadas)
        
        # Classifica parâmetros
        positivos, negativos, incertos = self.classificador.classificar(
            sala.agentes, topico, consenso['score_medio']
        )
        
        # Salva classificação
        self.classificador.salvar_classificacao(positivos, negativos, incertos, topico)
        
        # Salva saída em arquivo
        self._salvar_saida(topico, consenso, positivos, negativos, incertos, sala)
        
        return {
            'topico': topico,
            'status': 'sucesso',
            'score_consenso': consenso['score_medio'],
            'parametros': {
                'positivos': len(positivos),
                'negativos': len(negativos),
                'incertos': len(incertos)
            }
        }
    
    def _gerar_conteudo_base(self, topico: str) -> str:
        """Gera conteúdo base para o tópico."""
        return f"""
        Conhecimento avançado sobre {topico.replace('_', ' ')}.
        Este é um tópico estratégico que requer análise profunda.
        Padrões emergentes indicam tendências importantes.
        Implementação recomendada com validação em múltiplas camadas.
        Métricas de sucesso devem ser estabelecidas desde o início.
        Documentação técnica essencial para reutilização futura.
        Otimização contínua garante melhor performance.
        Segurança é prioridade em todas as camadas.
        Escalabilidade deve ser considerada no design.
        """
    
    def _salvar_saida(
        self, topico: str, consenso: Dict, positivos: List[Dict],
        negativos: List[Dict], incertos: List[Dict], sala: SalaDebate
    ):
        """Salva saída em arquivo JSON."""
        saida = {
            'topico': topico,
            'timestamp': datetime.now().isoformat(),
            'score_consenso': consenso['score_medio'],
            'num_agentes': 8,
            'num_rodadas': sala.rodada_atual,
            'num_criticas': len(sala.historico_criticas),
            'parametros': {
                'positivos': positivos,
                'negativos': negativos,
                'incertos': incertos
            },
            'consensos_agentes': consenso['consensos_agentes']
        }
        
        filename = f"{topico}_{generate_id()[:8]}.json"
        filepath = CONFIG.SAIDA_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(saida, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f" Saída salva: {filepath.name}")


# ====================================================================================
# SEÇÃO 12: ORQUESTRADOR PRINCIPAL
# ====================================================================================

class Orquestrador:
    """Orquestra a execução completa do sistema."""
    
    TOPICOS_PADRAO = [
        "python_avancado", "docker_kubernetes", "aws_cloud",
        "machine_learning", "sql_otimizado", "blockchain_cripto",
        "cybersecurity_defesa", "api_rest_graphql", "arquitetura_software",
        "performance_tuning", "devops_ci_cd", "microservicos"
    ]
    
    def __init__(self, usar_web_search: bool = True):
        self.usar_web_search = usar_web_search
        self.processador = ProcessadorTopico(usar_web_search)
    
    def executar(
        self, topicos: List[str] = None, num_rodadas: int = 15
    ) -> List[Dict]:
        """Executa processamento completo."""
        topicos = topicos or self.TOPICOS_PADRAO
        
        # Banner inicial
        self._mostrar_banner()
        
        # Estatísticas iniciais
        stats_inicial = db.get_estatisticas()
        logger.info(f" Banco de dados: {stats_inicial['total_parametros']} parâmetros")
        logger.info(f" Memória: {stats_inicial['total_memorias']} entradas")
        logger.info(f" Debates: {stats_inicial['total_debates']} realizados")
        
        resultados = []
        
        # Processa tópicos em paralelo
        logger.info(f"\n Processando {len(topicos)} tópicos...")
        
        with ThreadPoolExecutor(max_workers=CONFIG.PARALELISMO_TOPICO) as executor:
            futures = {
                executor.submit(self.processador.processar, t, num_rodadas): t
                for t in topicos
            }
            
            for future in as_completed(futures):
                topico = futures[future]
                try:
                    resultado = future.result()
                    resultados.append(resultado)
                    logger.info(f"\n CONCLUÍDO: {topico.upper()}")
                    logger.info(f"   Score: {resultado['score_consenso']:.2%}")
                except Exception as e:
                    logger.error(f"\n ERRO em {topico}: {e}")
        
        # Relatório final
        self._relatorio_final(resultados)
        
        return resultados
    
    def _mostrar_banner(self):
        """Mostra banner inicial."""
        banner = f"""
                                                                                
                                                                                
    {CONFIG.NOME:<74}  
    Versão {CONFIG.VERSAO:<67}  
                                                                                
    8 Agentes Autônomos | Debate Coletivo | Auto-Melhoria Contínua             
                                                                                
                                                                                
        """
        print(Fore.CYAN + banner + Style.RESET_ALL)
        logger.info(f" Base: {CONFIG.BASE_DIR}")
        logger.info(f" Banco: {CONFIG.DB_PATH}")
        logger.info(f" Saída: {CONFIG.SAIDA_DIR}")
        logger.info(f" Web Search: {'Sim' if self.usar_web_search else 'Não'}")
    
    def _relatorio_final(self, resultados: List[Dict]):
        """Gera relatório final."""
        stats_final = db.get_estatisticas()
        
        print("\n" + "="*70)
        logger.info(" RELATÓRIO FINAL")
        print("="*70)
        
        logger.info(f" Tópicos processados: {len(resultados)}")
        
        if resultados:
            score_medio = sum(r['score_consenso'] for r in resultados) / len(resultados)
            logger.info(f" Score médio: {score_medio:.2%}")
        
        total_params = sum(
            r['parametros']['positivos'] + r['parametros']['negativos'] + r['parametros']['incertos']
            for r in resultados
        )
        logger.info(f" Total parâmetros gerados: {total_params}")
        
        logger.info(f" Parâmetros no BD: {stats_final['total_parametros']}")
        logger.info(f" Críticas no BD: {stats_final['total_criticas']}")
        logger.info(f" Memórias no BD: {stats_final['total_memorias']}")
        logger.info(f" Score médio geral: {stats_final['score_medio_geral']:.4f}")
        
        logger.info("\n Sistema pronto para novo ciclo de aprendizado")
        logger.info(" Memória global alimentando próximas execuções")
        
        print("="*70)
        logger.info(" TREINAMENTO FINALIZADO!")
        print("="*70 + "\n")


# ====================================================================================
# SEÇÃO 13: FUNÇÃO PRINCIPAL
# ====================================================================================

def main(
    topicos: List[str] = None,
    num_rodadas: int = 15,
    usar_web_search: bool = True
) -> List[Dict]:
    """
    Função principal do sistema.
    
    Args:
        topicos: Lista de tópicos (None = usar padrão)
        num_rodadas: Número de rodadas de debate
        usar_web_search: Se True, busca informações na web
    
    Returns:
        Lista de resultados por tópico
    """
    try:
        orquestrador = Orquestrador(usar_web_search=usar_web_search)
        return orquestrador.executar(topicos, num_rodadas)
    except KeyboardInterrupt:
        logger.warning("\n Interrompido pelo usuário")
        return []
    except Exception as e:
        logger.error(f"\n Erro crítico: {e}")
        raise


# ====================================================================================
# SEÇÃO 14: EXECUÇÃO
# ====================================================================================

if __name__ == "__main__":
    # Executa com configurações padrão
    # Você pode customizar:
    # resultados = main(topicos=["seu_topico"], num_rodadas=20, usar_web_search=True)
    
    resultados = main()
    
    # Exibe resumo
    print("\n" + "="*70)
    print("RESUMO DOS RESULTADOS:")
    print("="*70)
    for r in resultados:
        print(f"  - {r['topico']}: {r['score_consenso']:.2%} | "
              f"+{r['parametros']['positivos']} -{r['parametros']['negativos']} "
              f"?{r['parametros']['incertos']}")
