"""
Models SQLAlchemy para o Sistema Multi-Agente.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Column, String, Float, Integer, DateTime, 
    Text, Boolean, ForeignKey, JSON, Index, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class JSONEncoder:
    """Helper para codificar/decodificar JSON."""
    
    @staticmethod
    def encode(data: Any) -> str:
        return json.dumps(data, ensure_ascii=False, default=str)
    
    @staticmethod
    def decode(data: str) -> Any:
        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return {}


class Parametro(Base):
    """Modelo para parâmetros gerados pelos agentes."""
    
    __tablename__ = 'parametros'
    
    id = Column(String(32), primary_key=True)
    topico = Column(String(255), nullable=False, index=True)
    tipo_param = Column(String(50), nullable=False, index=True)  # positivo, negativo, incerto
    conteudo = Column(JSON, nullable=False)
    score = Column(Float, default=0.0, index=True)
    score_detalhado = Column(JSON, default=dict)  # scores individuais
    criados_por = Column(String(500))  # Lista de agentes separados por vírgula
    criticados_por = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    rodada_debate = Column(Integer, default=1)
    versao = Column(Integer, default=1)
    
    # Metadados
    fonte = Column(String(255))  # web, gerado, hibrido
    url_fonte = Column(String(1000))
    validado = Column(Boolean, default=False)
    usos = Column(Integer, default=0)  # Quantas vezes foi usado
    
    # Relacionamentos
    criticas = relationship("Critica", back_populates="parametro", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_parametros_topico_tipo', 'topico', 'tipo_param'),
        Index('idx_parametros_score', 'score', 'tipo_param'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'topico': self.topico,
            'tipo': self.tipo_param,
            'conteudo': self.conteudo,
            'score': self.score,
            'score_detalhado': self.score_detalhado,
            'criados_por': self.criados_por.split(',') if self.criados_por else [],
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'rodada': self.rodada_debate,
            'fonte': self.fonte,
            'validado': self.validado,
            'usos': self.usos
        }
    
    def incrementar_uso(self):
        """Incrementa contador de usos."""
        self.usos += 1


class Critica(Base):
    """Modelo para críticas entre agentes."""
    
    __tablename__ = 'criticas'
    
    id = Column(String(32), primary_key=True)
    parametro_id = Column(String(32), ForeignKey('parametros.id'), nullable=True, index=True)
    debate_id = Column(String(32), ForeignKey('ciclos_debate.id'), nullable=True, index=True)
    
    de_agente = Column(String(100), nullable=False, index=True)
    para_agente = Column(String(100), nullable=False, index=True)
    para_topico = Column(String(255), nullable=False, index=True)
    
    tipo_critica = Column(String(50), default='construtiva')  # construtiva, positiva, negativa
    pontos_positivos = Column(JSON, default=list)
    pontos_negativos = Column(JSON, default=list)
    sugestoes = Column(JSON, default=list)
    score_qualidade = Column(Float, default=0.5)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    rodada = Column(Integer, default=1)
    
    # Relacionamentos
    parametro = relationship("Parametro", back_populates="criticas")
    debate = relationship("CicloDebate", back_populates="criticas")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'de': self.de_agente,
            'para': self.para_agente,
            'topico': self.para_topico,
            'tipo': self.tipo_critica,
            'positivos': self.pontos_positivos,
            'negativos': self.pontos_negativos,
            'sugestoes': self.sugestoes,
            'score': self.score_qualidade,
            'rodada': self.rodada
        }


class CicloDebate(Base):
    """Modelo para ciclos completos de debate."""
    
    __tablename__ = 'ciclos_debate'
    
    id = Column(String(32), primary_key=True)
    topico = Column(String(255), nullable=False, index=True)
    rodada = Column(Integer, default=1)
    num_criticas = Column(Integer, default=0)
    
    # Consenso
    consenso_final = Column(JSON)
    score_consenso = Column(Float, default=0.0)
    agentes_participantes = Column(String(500))
    
    # Metadados
    timestamp_inicio = Column(DateTime, default=datetime.utcnow)
    timestamp_fim = Column(DateTime)
    duracao_segundos = Column(Float)
    
    # Status
    status = Column(String(50), default='em_andamento')  # em_andamento, concluido, cancelado
    
    # Relacionamentos
    criticas = relationship("Critica", back_populates="debate")
    
    __table_args__ = (
        Index('idx_debate_topico_rodada', 'topico', 'rodada'),
    )
    
    def finalizar(self, score: float):
        """Finaliza o ciclo de debate."""
        self.timestamp_fim = datetime.utcnow()
        self.duracao_segundos = (self.timestamp_fim - self.timestamp_inicio).total_seconds()
        self.score_consenso = score
        self.status = 'concluido'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'topico': self.topico,
            'rodada': self.rodada,
            'num_criticas': self.num_criticas,
            'score_consenso': self.score_consenso,
            'status': self.status,
            'duracao': self.duracao_segundos,
            'inicio': self.timestamp_inicio.isoformat() if self.timestamp_inicio else None,
            'fim': self.timestamp_fim.isoformat() if self.timestamp_fim else None
        }


class MemoriaGlobal(Base):
    """Modelo para memória global do sistema."""
    
    __tablename__ = 'memoria_global'
    
    id = Column(String(32), primary_key=True)
    tipo = Column(String(100), nullable=False, index=True)  # padrao, fato, regra, experiencia
    dados = Column(JSON, nullable=False)
    
    # Relevância e acesso
    relevancia = Column(Float, default=1.0, index=True)
    acessos = Column(Integer, default=0)
    ultima_atualizacao = Column(DateTime, default=datetime.utcnow)
    
    # Tags para busca
    tags = Column(String(1000))
    topico_relacionado = Column(String(255), index=True)
    
    # Origem
    fonte = Column(String(255))
    agente_origem = Column(String(100))
    
    __table_args__ = (
        Index('idx_memoria_tipo_relevancia', 'tipo', 'relevancia'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'tipo': self.tipo,
            'dados': self.dados,
            'relevancia': self.relevancia,
            'acessos': self.acessos,
            'tags': self.tags.split(',') if self.tags else [],
            'topico': self.topico_relacionado
        }
    
    def acessar(self):
        """Registra acesso à memória."""
        self.acessos += 1
        self.ultima_atualizacao = datetime.utcnow()


class AgentePerformance(Base):
    """Modelo para tracking de performance dos agentes."""
    
    __tablename__ = 'agente_performance'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    agente_nome = Column(String(100), nullable=False, index=True)
    agente_id = Column(Integer, nullable=False)
    
    # Métricas
    total_debates = Column(Integer, default=0)
    total_criticas_geradas = Column(Integer, default=0)
    total_criticas_recebidas = Column(Integer, default=0)
    
    # Scores
    score_medio = Column(Float, default=0.5)
    acuracia = Column(Float, default=0.5)
    credibilidade = Column(Float, default=1.0)
    
    # Histórico
    acertos = Column(Integer, default=0)
    erros = Column(Integer, default=0)
    
    # Timestamps
    primeiro_debate = Column(DateTime)
    ultimo_debate = Column(DateTime)
    
    __table_args__ = (
        Index('idx_performance_agente', 'agente_nome', 'agente_id'),
    )
    
    def atualizar_score(self, novo_score: float):
        """Atualiza score médio com média móvel."""
        n = self.total_debates
        self.score_medio = (self.score_medio * n + novo_score) / (n + 1)
        self.total_debates += 1
    
    def registrar_acerto(self):
        """Registra um acerto."""
        self.acertos += 1
        self._atualizar_acuracia()
    
    def registrar_erro(self):
        """Registra um erro."""
        self.erros += 1
        self._atualizar_acuracia()
    
    def _atualizar_acuracia(self):
        """Recalcula acurácia."""
        total = self.acertos + self.erros
        if total > 0:
            self.acuracia = self.acertos / total


class BuscaWebCache(Base):
    """Cache para buscas web."""
    
    __tablename__ = 'busca_web_cache'
    
    id = Column(String(32), primary_key=True)
    query = Column(String(1000), nullable=False, index=True)
    resultados = Column(JSON, nullable=False)
    
    # Metadados
    timestamp = Column(DateTime, default=datetime.utcnow)
    ttl = Column(Integer, default=86400)  # Tempo de vida em segundos
    usos = Column(Integer, default=0)
    
    def is_expirado(self) -> bool:
        """Verifica se o cache expirou."""
        from datetime import timedelta
        expiracao = self.timestamp + timedelta(seconds=self.ttl)
        return datetime.utcnow() > expiracao
    
    def acessar(self):
        """Registra acesso ao cache."""
        self.usos += 1


# Índices adicionais para performance
# Estes serão criados automaticamente pelo SQLAlchemy
