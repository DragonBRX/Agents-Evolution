"""
Gerenciador de banco de dados com SQLAlchemy.
"""

import hashlib
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy import create_engine, func, desc, and_
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.pool import StaticPool

from .models import Base, Parametro, Critica, CicloDebate, MemoriaGlobal, AgentePerformance, BuscaWebCache

T = TypeVar('T')


class DatabaseManager:
    """
    Gerenciador centralizado de banco de dados.
    Suporta SQLite e PostgreSQL com connection pooling.
    """
    
    _instance: Optional['DatabaseManager'] = None
    _engine = None
    _session_factory = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(
        self,
        db_url: Optional[str] = None,
        sqlite_path: Optional[str] = None,
        echo: bool = False,
        pool_size: int = 10
    ):
        if self._engine is not None:
            return
            
        # Determina URL do banco
        if db_url:
            self.db_url = db_url
        elif sqlite_path:
            # Garante que o diretório existe
            Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)
            self.db_url = f"sqlite:///{sqlite_path}"
        else:
            self.db_url = "sqlite:///data/flash_sistema.db"
        
        # Cria engine
        if self.db_url.startswith('sqlite'):
            self._engine = create_engine(
                self.db_url,
                echo=echo,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool
            )
        else:
            self._engine = create_engine(
                self.db_url,
                echo=echo,
                pool_size=pool_size,
                max_overflow=20
            )
        
        # Cria session factory
        self._session_factory = sessionmaker(bind=self._engine)
        
        # Cria tabelas
        self._create_tables()
    
    def _create_tables(self):
        """Cria todas as tabelas se não existirem."""
        Base.metadata.create_all(self._engine)
    
    @contextmanager
    def session(self) -> Session:
        """Context manager para sessões de banco de dados."""
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_session(self) -> Session:
        """Retorna uma nova sessão (não gerenciada)."""
        return self._session_factory()
    
    # =========================================================================
    # Operações com Parâmetros
    # =========================================================================
    
    def salvar_parametro(
        self,
        topico: str,
        tipo: str,
        conteudo: Dict[str, Any],
        score: float,
        criados_por: List[str],
        fonte: str = "gerado",
        rodada: int = 1,
        url_fonte: Optional[str] = None
    ) -> str:
        """Salva um novo parâmetro no banco."""
        param_id = hashlib.sha256(
            f"{tipo}_{topico}_{time.time()}".encode()
        ).hexdigest()[:16]
        
        with self.session() as session:
            param = Parametro(
                id=param_id,
                topico=topico,
                tipo_param=tipo,
                conteudo=conteudo,
                score=score,
                criados_por=','.join(criados_por),
                fonte=fonte,
                rodada_debate=rodada,
                url_fonte=url_fonte
            )
            session.add(param)
        
        return param_id
    
    def buscar_parametros(
        self,
        topico: Optional[str] = None,
        tipo: Optional[str] = None,
        min_score: Optional[float] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Parametro]:
        """Busca parâmetros com filtros."""
        with self.session() as session:
            query = session.query(Parametro)
            
            if topico:
                query = query.filter(Parametro.topico == topico)
            if tipo:
                query = query.filter(Parametro.tipo_param == tipo)
            if min_score is not None:
                query = query.filter(Parametro.score >= min_score)
            
            return query.order_by(desc(Parametro.score)).offset(offset).limit(limit).all()
    
    def buscar_parametros_por_topico(
        self,
        topico: str,
        limit: int = 100
    ) -> Dict[str, List[Dict]]:
        """Busca parâmetros organizados por tipo."""
        with self.session() as session:
            positivos = session.query(Parametro).filter(
                and_(Parametro.topico == topico, Parametro.tipo_param == 'positivo')
            ).order_by(desc(Parametro.score)).limit(limit).all()
            
            negativos = session.query(Parametro).filter(
                and_(Parametro.topico == topico, Parametro.tipo_param == 'negativo')
            ).order_by(desc(Parametro.score)).limit(limit).all()
            
            incertos = session.query(Parametro).filter(
                and_(Parametro.topico == topico, Parametro.tipo_param == 'incerto')
            ).order_by(desc(Parametro.score)).limit(limit).all()
            
            return {
                'positivos': [p.to_dict() for p in positivos],
                'negativos': [p.to_dict() for p in negativos],
                'incertos': [p.to_dict() for p in incertos]
            }
    
    def atualizar_score_parametro(self, param_id: str, novo_score: float):
        """Atualiza score de um parâmetro."""
        with self.session() as session:
            param = session.query(Parametro).filter(Parametro.id == param_id).first()
            if param:
                param.score = novo_score
    
    # =========================================================================
    # Operações com Críticas
    # =========================================================================
    
    def salvar_critica(
        self,
        de_agente: str,
        para_agente: str,
        para_topico: str,
        pontos_positivos: List[str],
        pontos_negativos: List[str],
        sugestoes: List[str],
        score_qualidade: float,
        rodada: int = 1,
        parametro_id: Optional[str] = None
    ) -> str:
        """Salva uma crítica no banco."""
        critica_id = hashlib.sha256(
            f"{de_agente}_{para_agente}_{time.time()}".encode()
        ).hexdigest()[:16]
        
        with self.session() as session:
            critica = Critica(
                id=critica_id,
                de_agente=de_agente,
                para_agente=para_agente,
                para_topico=para_topico,
                pontos_positivos=pontos_positivos,
                pontos_negativos=pontos_negativos,
                sugestoes=sugestoes,
                score_qualidade=score_qualidade,
                rodada=rodada,
                parametro_id=parametro_id
            )
            session.add(critica)
        
        return critica_id
    
    def buscar_criticas_por_agente(
        self,
        agente_nome: str,
        como_destinatario: bool = True,
        limit: int = 100
    ) -> List[Critica]:
        """Busca críticas de ou para um agente."""
        with self.session() as session:
            if como_destinatario:
                return session.query(Critica).filter(
                    Critica.para_agente == agente_nome
                ).order_by(desc(Critica.timestamp)).limit(limit).all()
            else:
                return session.query(Critica).filter(
                    Critica.de_agente == agente_nome
                ).order_by(desc(Critica.timestamp)).limit(limit).all()
    
    # =========================================================================
    # Operações com Ciclos de Debate
    # =========================================================================
    
    def criar_ciclo_debate(self, topico: str, rodada: int = 1) -> str:
        """Cria um novo ciclo de debate."""
        debate_id = hashlib.sha256(
            f"{topico}_{rodada}_{time.time()}".encode()
        ).hexdigest()[:16]
        
        with self.session() as session:
            debate = CicloDebate(
                id=debate_id,
                topico=topico,
                rodada=rodada
            )
            session.add(debate)
        
        return debate_id
    
    def finalizar_ciclo_debate(
        self,
        debate_id: str,
        score_consenso: float,
        consenso: Dict[str, Any],
        agentes: List[str]
    ):
        """Finaliza um ciclo de debate."""
        with self.session() as session:
            debate = session.query(CicloDebate).filter(CicloDebate.id == debate_id).first()
            if debate:
                debate.finalizar(score_consenso)
                debate.consenso_final = consenso
                debate.agentes_participantes = ','.join(agentes)
    
    def buscar_debates_por_topico(self, topico: str) -> List[CicloDebate]:
        """Busca todos os debates de um tópico."""
        with self.session() as session:
            return session.query(CicloDebate).filter(
                CicloDebate.topico == topico
            ).order_by(desc(CicloDebate.timestamp_inicio)).all()
    
    # =========================================================================
    # Operações com Memória Global
    # =========================================================================
    
    def salvar_memoria(
        self,
        tipo: str,
        dados: Dict[str, Any],
        relevancia: float = 1.0,
        tags: Optional[List[str]] = None,
        topico: Optional[str] = None,
        fonte: Optional[str] = None,
        agente_origem: Optional[str] = None
    ) -> str:
        """Salva uma entrada na memória global."""
        mem_id = hashlib.sha256(
            f"{tipo}_{time.time()}".encode()
        ).hexdigest()[:16]
        
        with self.session() as session:
            memoria = MemoriaGlobal(
                id=mem_id,
                tipo=tipo,
                dados=dados,
                relevancia=relevancia,
                tags=','.join(tags) if tags else None,
                topico_relacionado=topico,
                fonte=fonte,
                agente_origem=agente_origem
            )
            session.add(memoria)
        
        return mem_id
    
    def buscar_memoria(
        self,
        tipo: Optional[str] = None,
        topico: Optional[str] = None,
        min_relevancia: float = 0.0,
        limit: int = 100
    ) -> List[MemoriaGlobal]:
        """Busca entradas na memória global."""
        with self.session() as session:
            query = session.query(MemoriaGlobal)
            
            if tipo:
                query = query.filter(MemoriaGlobal.tipo == tipo)
            if topico:
                query = query.filter(MemoriaGlobal.topico_relacionado == topico)
            
            query = query.filter(MemoriaGlobal.relevancia >= min_relevancia)
            
            return query.order_by(desc(MemoriaGlobal.relevancia)).limit(limit).all()
    
    def recuperar_memoria_para_agente(
        self,
        topico: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Recupera memória relevante para um agente processar um tópico."""
        with self.session() as session:
            memorias = session.query(MemoriaGlobal).filter(
                MemoriaGlobal.topico_relacionado == topico
            ).order_by(desc(MemoriaGlobal.relevancia)).limit(limit).all()
            
            # Atualiza acessos
            for mem in memorias:
                mem.acessar()
            
            return [m.to_dict() for m in memorias]
    
    # =========================================================================
    # Operações com Performance de Agentes
    # =========================================================================
    
    def atualizar_performance_agente(
        self,
        agente_nome: str,
        agente_id: int,
        novo_score: float,
        acerto: Optional[bool] = None
    ):
        """Atualiza performance de um agente."""
        with self.session() as session:
            perf = session.query(AgentePerformance).filter(
                and_(
                    AgentePerformance.agente_nome == agente_nome,
                    AgentePerformance.agente_id == agente_id
                )
            ).first()
            
            if not perf:
                perf = AgentePerformance(
                    agente_nome=agente_nome,
                    agente_id=agente_id,
                    primeiro_debate=func.now()
                )
                session.add(perf)
            
            perf.atualizar_score(novo_score)
            perf.ultimo_debate = func.now()
            
            if acerto is not None:
                if acerto:
                    perf.registrar_acerto()
                else:
                    perf.registrar_erro()
    
    def get_performance_agente(self, agente_nome: str) -> Optional[Dict[str, Any]]:
        """Retorna performance de um agente."""
        with self.session() as session:
            perf = session.query(AgentePerformance).filter(
                AgentePerformance.agente_nome == agente_nome
            ).order_by(desc(AgentePerformance.ultimo_debate)).first()
            
            if perf:
                return {
                    'agente': perf.agente_nome,
                    'total_debates': perf.total_debates,
                    'score_medio': perf.score_medio,
                    'acuracia': perf.acuracia,
                    'credibilidade': perf.credibilidade,
                    'acertos': perf.acertos,
                    'erros': perf.erros
                }
            return None
    
    # =========================================================================
    # Cache de Busca Web
    # =========================================================================
    
    def get_cache_busca(self, query: str) -> Optional[List[Dict]]:
        """Busca resultado em cache."""
        with self.session() as session:
            cache = session.query(BuscaWebCache).filter(
                BuscaWebCache.query == query
            ).first()
            
            if cache and not cache.is_expirado():
                cache.acessar()
                return cache.resultados
            
            return None
    
    def salvar_cache_busca(
        self,
        query: str,
        resultados: List[Dict],
        ttl: int = 86400
    ):
        """Salva resultado de busca em cache."""
        cache_id = hashlib.sha256(query.encode()).hexdigest()[:16]
        
        with self.session() as session:
            # Remove cache antigo se existir
            session.query(BuscaWebCache).filter(
                BuscaWebCache.query == query
            ).delete()
            
            cache = BuscaWebCache(
                id=cache_id,
                query=query,
                resultados=resultados,
                ttl=ttl
            )
            session.add(cache)
    
    # =========================================================================
    # Estatísticas
    # =========================================================================
    
    def get_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais do banco."""
        with self.session() as session:
            total_parametros = session.query(Parametro).count()
            total_criticas = session.query(Critica).count()
            total_debates = session.query(CicloDebate).count()
            total_memorias = session.query(MemoriaGlobal).count()
            
            score_medio = session.query(func.avg(Parametro.score)).scalar() or 0
            
            return {
                'total_parametros': total_parametros,
                'total_criticas': total_criticas,
                'total_debates': total_debates,
                'total_memorias': total_memorias,
                'score_medio_geral': round(score_medio, 4)
            }


# Instância global
_db_instance: Optional[DatabaseManager] = None


def get_db() -> DatabaseManager:
    """Retorna instância singleton do DatabaseManager."""
    global _db_instance
    if _db_instance is None:
        from ..config import get_config
        config = get_config()
        
        sqlite_path = config.db_path
        echo_sql = config.get('banco_dados', 'config', 'echo_sql', default=False)
        
        _db_instance = DatabaseManager(
            sqlite_path=sqlite_path,
            echo=echo_sql
        )
    return _db_instance


def init_db(db_url: Optional[str] = None, sqlite_path: Optional[str] = None):
    """Inicializa o banco de dados."""
    global _db_instance
    _db_instance = DatabaseManager(db_url=db_url, sqlite_path=sqlite_path)
    return _db_instance
