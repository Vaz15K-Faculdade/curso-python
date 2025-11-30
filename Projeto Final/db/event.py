from typing import Optional, List
from datetime import datetime
from datetime import date as date_type
from decimal import Decimal

from sqlalchemy import Text, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel

from db.events_database import EventBase


class Event(EventBase):
    __tablename__ = "event"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data: Mapped[date_type] = mapped_column(nullable=False)
    hora: Mapped[str] = mapped_column(nullable=False)  # Formato "HH:MM"
    localizacao: Mapped[str] = mapped_column(nullable=False)
    preco: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)  # Preço base (será sobrescrito pelos lotes)
    url_imagem: Mapped[Optional[str]] = mapped_column(nullable=True)
    ativo: Mapped[bool] = mapped_column(default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relacionamentos com tickets
    ticket_batches: Mapped[List["LoteIngresso"]] = relationship("LoteIngresso", back_populates="event", cascade="all, delete-orphan")
    tickets: Mapped[List["Ingresso"]] = relationship("Ingresso", back_populates="event", cascade="all, delete-orphan")
    
    @property
    def total_ingressos(self) -> int:
        """Retorna o total de ingressos disponíveis para o evento"""
        return sum(batch.total_ingressos for batch in self.ticket_batches)
    
    @property
    def ingressos_vendidos(self) -> int:
        """Retorna o total de ingressos vendidos"""
        return sum(batch.ingressos_vendidos for batch in self.ticket_batches)
    
    @property
    def ingressos_disponiveis(self) -> int:
        """Retorna o total de ingressos disponíveis"""
        return self.total_ingressos - self.ingressos_vendidos
    
    @property
    def lote_atual(self) -> Optional["LoteIngresso"]:
        """Retorna o lote atual em vendas"""
        for batch in sorted(self.ticket_batches, key=lambda b: b.numero_lote):
            if batch.status == "active" and batch.ingressos_disponiveis > 0:
                return batch
        return None
    
    @property
    def preco_atual(self) -> Decimal:
        """Retorna o preço atual do ingresso (do lote ativo)"""
        current = self.lote_atual
        return current.preco if current else self.preco


class EventoCreate(BaseModel):
    name: str
    description: Optional[str] = None
    data: date_type
    hora: str
    localizacao: str
    preco: float
    url_imagem: Optional[str] = None
    ativo: bool = True


class EventoUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    data: Optional[date_type] = None
    hora: Optional[str] = None
    localizacao: Optional[str] = None
    preco: Optional[float] = None
    url_imagem: Optional[str] = None
    ativo: Optional[bool] = None


class EventoRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    data: date_type
    hora: str
    localizacao: str
    preco: float
    url_imagem: Optional[str]
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True
