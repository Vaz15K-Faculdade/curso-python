from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.events_database import get_sessao_eventos
from db.event import Event, EventoCreate, EventoUpdate, EventoRead
from db.user import User
from db.auth_config import usuario_ativo

async def get_admin_operador(current_user: User = Depends(usuario_ativo)):
    if not (current_user.is_superuser or current_user.is_operator):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores e operadores podem gerenciar eventos."
        )
    return current_user

event_router = APIRouter(prefix="/events", tags=["events"])


@event_router.get("/", response_model=List[EventoRead])
async def get_eventos(
    session: AsyncSession = Depends(get_sessao_eventos),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True
):
    """Lista todos os eventos (público)"""
    query = select(Event)
    
    if active_only:
        query = query.where(Event.ativo == True)
    
    query = query.offset(skip).limit(limit).order_by(Event.data.asc(), Event.hora.asc())
    
    result = await session.execute(query)
    events = result.scalars().all()
    
    return events


@event_router.get("/{event_id}", response_model=EventoRead)
async def get_evento(
    event_id: int,
    session: AsyncSession = Depends(get_sessao_eventos)
):
    """Obtém um evento específico"""
    result = await session.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    
    return event


@event_router.post("/", response_model=EventoRead, status_code=status.HTTP_201_CREATED)
async def criar_evento(
    event_data: EventoCreate,
    session: AsyncSession = Depends(get_sessao_eventos),
    current_user: User = Depends(get_admin_operador)
):
    """Cria um novo evento (apenas admin/operador)"""
    
    # Converte os dados do Pydantic para SQLAlchemy
    event_dict = event_data.model_dump()
    
    # Cria o evento
    event = Event(**event_dict)
    session.add(event)
    
    try:
        await session.commit()
        await session.refresh(event)
        return event
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar evento: {str(e)}"
        )


@event_router.put("/{event_id}", response_model=EventoRead)
async def atualizar_evento(
    event_id: int,
    event_data: EventoUpdate,
    session: AsyncSession = Depends(get_sessao_eventos),
    current_user: User = Depends(get_admin_operador)
):
    """Atualiza um evento (apenas admin/operador)"""
    
    # Busca o evento
    result = await session.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    
    # Atualiza apenas os campos fornecidos
    update_data = event_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    try:
        await session.commit()
        await session.refresh(event)
        return event
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar evento: {str(e)}"
        )


@event_router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_evento(
    event_id: int,
    session: AsyncSession = Depends(get_sessao_eventos),
    current_user: User = Depends(get_admin_operador)
):
    """Remove um evento (apenas admin/operador)"""
    
    # Busca o evento
    result = await session.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    
    try:
        await session.delete(event)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao remover evento: {str(e)}"
        )


@event_router.patch("/{event_id}/toggle-active", response_model=EventoRead)
async def alternar_status_evento(
    event_id: int,
    session: AsyncSession = Depends(get_sessao_eventos),
    current_user: User = Depends(get_admin_operador)
):
    """Ativa/desativa um evento (apenas admin/operador)"""
    
    # Busca o evento
    result = await session.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    
    # Inverte o status
    event.ativo = not event.ativo
    
    try:
        await session.commit()
        await session.refresh(event)
        return event
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao alterar status do evento: {str(e)}"
        )
