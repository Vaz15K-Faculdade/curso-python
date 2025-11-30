from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

EVENTS_DATABASE_URL = "sqlite+aiosqlite:///./events.db"


class EventBase(DeclarativeBase):
    pass


events_engine = create_async_engine(EVENTS_DATABASE_URL)
events_async_session_maker = async_sessionmaker(events_engine, expire_on_commit=False)


async def create_events_db_and_tables():
    """Cria o banco de dados e tabelas de eventos"""
    from db.event import Event
    from db.ticket import LoteIngresso, Ingresso
    
    async with events_engine.begin() as conn:
        await conn.run_sync(EventBase.metadata.create_all)


async def get_sessao_eventos() -> AsyncGenerator[AsyncSession, None]:
    """Retorna uma sessão async para o banco de eventos"""
    async with events_async_session_maker() as session:
        yield session
