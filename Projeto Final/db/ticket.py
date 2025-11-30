from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import Text, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel

from db.events_database import EventBase
from db.event import EventoRead


class StatusLoteIngresso(str, Enum):
    """Status do lote de ingressos"""
    WAITING = "waiting"  # Aguardando (não iniciou vendas ainda)
    ACTIVE = "active"    # Ativo (vendendo)
    SOLD_OUT = "sold_out"  # Esgotado
    EXPIRED = "expired"  # Expirado


class LoteIngresso(EventBase):
    """Lote de ingressos para um evento"""
    __tablename__ = "ticket_batch"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), nullable=False)
    numero_lote: Mapped[int] = mapped_column(nullable=False)  # Número do lote (1, 2, 3...)
    name: Mapped[str] = mapped_column(nullable=False)  # Ex: "1º Lote", "Lote Promocional"
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Quantidade e vendas
    total_ingressos: Mapped[int] = mapped_column(nullable=False)  # Total de ingressos neste lote
    ingressos_vendidos: Mapped[int] = mapped_column(default=0, nullable=False)  # Ingressos vendidos
    
    # Preço
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    
    # Status e controle
    status: Mapped[StatusLoteIngresso] = mapped_column(default=StatusLoteIngresso.WAITING, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    # Datas
    data_inicio_venda: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    data_fim_venda: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    event: Mapped["Event"] = relationship("Event", back_populates="ticket_batches")
    tickets: Mapped[List["Ingresso"]] = relationship("Ingresso", back_populates="batch")
    
    # Garante que não há lotes duplicados por evento
    __table_args__ = (
        UniqueConstraint('event_id', 'numero_lote', name='unique_event_batch'),
    )
    
    @property
    def ingressos_disponiveis(self) -> int:
        """Retorna a quantidade de ingressos disponíveis"""
        return self.total_ingressos - self.ingressos_vendidos
    
    @property
    def esgotado(self) -> bool:
        """Verifica se o lote está esgotado"""
        return self.ingressos_vendidos >= self.total_ingressos
    
    @property
    def porcentagem_progresso(self) -> float:
        """Retorna o percentual de vendas"""
        if self.total_ingressos == 0:
            return 0.0
        return (self.ingressos_vendidos / self.total_ingressos) * 100


class Ingresso(EventBase):
    """Ingresso individual"""
    __tablename__ = "ticket"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), nullable=False)
    batch_id: Mapped[int] = mapped_column(ForeignKey("ticket_batch.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)  # Referência ao usuário (não FK para manter bancos separados)
    
    # Informações do ingresso
    codigo_ingresso: Mapped[str] = mapped_column(unique=True, nullable=False)  # Código único do ingresso
    qr_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # QR code em base64
    numero_assento: Mapped[Optional[str]] = mapped_column(nullable=True)  # Número do assento (se aplicável)
    
    # Valor pago e status
    valor_pago: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(default="active", nullable=False)  # active, canceled, used
    
    # Datas
    data_compra: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    data_uso: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Relacionamentos
    event: Mapped["Event"] = relationship("Event", back_populates="tickets")
    batch: Mapped["LoteIngresso"] = relationship("LoteIngresso", back_populates="tickets")


# Schemas Pydantic para API

class LoteIngressoCreate(BaseModel):
    event_id: int
    numero_lote: int
    name: str
    description: Optional[str] = None
    total_ingressos: int
    price: float
    status: Optional[StatusLoteIngresso] = StatusLoteIngresso.WAITING
    data_inicio_venda: Optional[datetime] = None
    data_fim_venda: Optional[datetime] = None


class LoteIngressoUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    total_ingressos: Optional[int] = None
    price: Optional[float] = None
    status: Optional[StatusLoteIngresso] = None
    is_active: Optional[bool] = None
    data_inicio_venda: Optional[datetime] = None
    data_fim_venda: Optional[datetime] = None


class LoteIngressoRead(BaseModel):
    id: int
    event_id: int
    numero_lote: int
    name: str
    description: Optional[str]
    total_ingressos: int
    ingressos_vendidos: int
    ingressos_disponiveis: int
    price: float
    status: StatusLoteIngresso
    is_active: bool
    porcentagem_progresso: float
    data_inicio_venda: Optional[datetime]
    data_fim_venda: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IngressoCreate(BaseModel):
    event_id: int
    quantity: int = 1
    batch_id: Optional[int] = None


class IngressoRead(BaseModel):
    id: int
    event_id: int
    batch_id: int
    user_id: int
    codigo_ingresso: str
    qr_code: Optional[str]
    numero_assento: Optional[str]
    valor_pago: float
    status: str
    data_compra: datetime
    data_uso: Optional[datetime]
    event: EventoRead

    class Config:
        from_attributes = True
