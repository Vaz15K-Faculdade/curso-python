from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
import secrets
import string
import qrcode
import io
import base64
from datetime import datetime

from db.events_database import get_sessao_eventos
from db.ticket import (LoteIngresso, Ingresso, LoteIngressoCreate,
                       LoteIngressoUpdate, LoteIngressoRead,
                       IngressoCreate, IngressoRead, StatusLoteIngresso)
from db.event import Event
from db.user import User
from db.auth_config import usuario_ativo

async def get_admin_operador(current_user: User = Depends(usuario_ativo)):
    if not (current_user.is_superuser or current_user.is_operator):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores e operadores podem gerenciar lotes de ingressos."
        )
    return current_user

ticket_router = APIRouter(prefix="/tickets", tags=["tickets"])


@ticket_router.get("/batches/event/{event_id}", response_model=List[LoteIngressoRead])
async def get_lotes_evento(
    event_id: int,
    session: AsyncSession = Depends(get_sessao_eventos)
):
    """Lista todos os lotes de um evento"""
    query = select(LoteIngresso).where(LoteIngresso.event_id == event_id).order_by(LoteIngresso.numero_lote)
    result = await session.execute(query)
    batches = result.scalars().all()
    return batches


@ticket_router.post("/batches/", response_model=LoteIngressoRead, status_code=status.HTTP_201_CREATED)
async def criar_lote_ingresso(
    dado_lote: LoteIngressoCreate,
    session: AsyncSession = Depends(get_sessao_eventos),
    current_user: User = Depends(get_admin_operador)
):
    """Cria um novo lote de ingressos"""
    
    # Verifica se o evento existe
    event_result = await session.execute(select(Event).where(Event.id == dado_lote.event_id))
    event = event_result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    
    # Verifica se já existe um lote com o mesmo número para este evento
    existing_batch = await session.execute(
        select(LoteIngresso).where(
            and_(
                LoteIngresso.event_id == dado_lote.event_id,
                LoteIngresso.numero_lote == dado_lote.numero_lote
            )
        )
    )
    
    if existing_batch.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um lote número {dado_lote.numero_lote} para este evento"
        )
    
    batch_dict = dado_lote.model_dump()
    
    # Usa o status fornecido pelo usuário ou define automaticamente
    if "status" not in batch_dict or batch_dict["status"] is None:
        # Define o status inicial baseado no número do lote
        if dado_lote.numero_lote == 1:
            batch_dict["status"] = StatusLoteIngresso.ACTIVE
        else:
            batch_dict["status"] = StatusLoteIngresso.WAITING
    
    batch = LoteIngresso(**batch_dict)
    session.add(batch)
    
    try:
        await session.commit()
        await session.refresh(batch)
        return batch
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar lote: {str(e)}"
        )


@ticket_router.put("/batches/{batch_id}", response_model=LoteIngressoRead)
async def atualizar_lote_ingresso(
    batch_id: int,
    dado_lote: LoteIngressoUpdate,
    session: AsyncSession = Depends(get_sessao_eventos),
    current_user: User = Depends(get_admin_operador)
):
    """Atualiza um lote de ingressos"""
    
    result = await session.execute(select(LoteIngresso).where(LoteIngresso.id == batch_id))
    batch = result.scalar_one_or_none()
    
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lote não encontrado"
        )
    
    # Atualiza apenas os campos fornecidos
    update_data = dado_lote.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(batch, field, value)
    
    try:
        await session.commit()
        await session.refresh(batch)
        return batch
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar lote: {str(e)}"
        )


@ticket_router.delete("/batches/{batch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_lote_ingresso(
    batch_id: int,
    session: AsyncSession = Depends(get_sessao_eventos),
    current_user: User = Depends(get_admin_operador)
):
    """Remove um lote de ingressos"""
    
    result = await session.execute(select(LoteIngresso).where(LoteIngresso.id == batch_id))
    batch = result.scalar_one_or_none()
    
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lote não encontrado"
        )
    
    # Verifica se há ingressos vendidos
    if batch.ingressos_vendidos > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível remover lote com ingressos já vendidos"
        )
    
    try:
        await session.delete(batch)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao remover lote: {str(e)}"
        )


def gerar_codigo_ingresso() -> str:
    """Gera um código único para o ingresso"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(8))


def gerar_qr_code(codigo_ingresso: str, event_name: str, user_name: str) -> str:
    """Gera um QR code para o ingresso e retorna em base64"""
    # Criar string dos dados
    qr_string = f"TICKET:{codigo_ingresso}|EVENT:{event_name}|USER:{user_name}|TIME:{datetime.now().isoformat()}"
    
    # Gerar QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_string)
    qr.make(fit=True)
    
    # Criar imagem
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Converter para base64
    buffer = io.BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)
    
    # Codificar em base64
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return qr_base64


async def get_lote_ativo_para_evento(event_id: int, session: AsyncSession) -> Optional[LoteIngresso]:
    """Retorna o lote ativo para um evento"""
    result = await session.execute(
        select(LoteIngresso).where(
            and_(
                LoteIngresso.event_id == event_id,
                LoteIngresso.status == StatusLoteIngresso.ACTIVE,
                LoteIngresso.is_active == True
            )
        ).order_by(LoteIngresso.numero_lote).limit(1)
    )
    return result.scalar_one_or_none()


async def verificar_e_avancar_lote(event_id: int, session: AsyncSession):
    """Verifica se o lote atual esgotou e avança para o próximo"""
    # Busca o lote atual
    current_batch = await get_lote_ativo_para_evento(event_id, session)
    
    if current_batch and current_batch.esgotado:
        # Marca o lote atual como esgotado
        current_batch.status = StatusLoteIngresso.SOLD_OUT
        
        # Busca o próximo lote
        next_batch_result = await session.execute(
            select(LoteIngresso).where(
                and_(
                    LoteIngresso.event_id == event_id,
                    LoteIngresso.numero_lote > current_batch.numero_lote,
                    LoteIngresso.status == StatusLoteIngresso.WAITING
                )
            ).order_by(LoteIngresso.numero_lote).limit(1)
        )
        
        next_batch = next_batch_result.scalar_one_or_none()
        if next_batch:
            next_batch.status = StatusLoteIngresso.ACTIVE
            
        await session.commit()


@ticket_router.post("/purchase/", response_model=List[IngressoRead], status_code=status.HTTP_201_CREATED)
async def comprar_ingressos(
    ticket_data: IngressoCreate,
    session: AsyncSession = Depends(get_sessao_eventos),
    current_user: User = Depends(usuario_ativo)
):
    """Compra ingressos para um evento"""
    
    # Verifica se o evento existe
    event_result = await session.execute(select(Event).where(Event.id == ticket_data.event_id))
    event = event_result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    
    # Busca o lote (específico ou ativo)
    if ticket_data.batch_id:
        # Compra de lote específico
        resultado_lote = await session.execute(
            select(LoteIngresso).where(
                and_(
                    LoteIngresso.id == ticket_data.batch_id,
                    LoteIngresso.event_id == ticket_data.event_id,
                    LoteIngresso.status == StatusLoteIngresso.ACTIVE,
                    LoteIngresso.is_active == True
                )
            )
        )
        lote_alvo = resultado_lote.scalar_one_or_none()
        
        if not lote_alvo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lote especificado não está disponível para venda"
            )
    else:
        # Busca o lote ativo automaticamente
        lote_alvo = await get_lote_ativo_para_evento(ticket_data.event_id, session)
        
        if not lote_alvo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não há ingressos disponíveis para este evento"
            )
    
    # Verifica disponibilidade
    if lote_alvo.ingressos_disponiveis < ticket_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Apenas {lote_alvo.ingressos_disponiveis} ingressos disponíveis no lote selecionado"
        )
    
    # Busca informações do evento para o QR code
    event_result = await session.execute(select(Event).where(Event.id == ticket_data.event_id))
    event = event_result.scalar_one_or_none()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    
    # Cria os ingressos
    ingressos = []
    for _ in range(ticket_data.quantity):
        codigo_ingresso = gerar_codigo_ingresso()
        
        # Garante que o código é único
        while True:
            existing = await session.execute(select(Ingresso).where(Ingresso.codigo_ingresso == codigo_ingresso))
            if not existing.scalar_one_or_none():
                break
            codigo_ingresso = gerar_codigo_ingresso()
        
        # Gera QR code para o ingresso
        qr_code_base64 = gerar_qr_code(codigo_ingresso, event.name, current_user.email)
        
        ingresso = Ingresso(
            event_id=ticket_data.event_id,
            batch_id=lote_alvo.id,
            user_id=current_user.id,
            codigo_ingresso=codigo_ingresso,
            qr_code=qr_code_base64,
            valor_pago=lote_alvo.price,
            status="active"
        )
        
        session.add(ingresso)
        ingressos.append(ingresso)
    
    # Atualiza contador do lote
    lote_alvo.ingressos_vendidos += ticket_data.quantity
    
    try:
        await session.commit()
        
        # Verifica se precisa avançar para o próximo lote
        await verificar_e_avancar_lote(ticket_data.event_id, session)
        
        # Atualiza os objetos com relacionamentos
        for ingresso in ingressos:
            await session.refresh(ingresso)
            
        # Recarrega os ingressos com relacionamentos
        result = await session.execute(
            select(Ingresso)
            .where(Ingresso.id.in_([ing.id for ing in ingressos]))
            .options(selectinload(Ingresso.event))
        )
        ingressos_com_event = result.scalars().all()
            
        return ingressos_com_event
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao comprar ingressos: {str(e)}"
        )


@ticket_router.get("/my-tickets/", response_model=List[IngressoRead])
async def get_meus_ingressos(
    session: AsyncSession = Depends(get_sessao_eventos),
    current_user: User = Depends(usuario_ativo)
):
    """Lista os ingressos do usuário logado"""
    result = await session.execute(
        select(Ingresso)
        .where(Ingresso.user_id == current_user.id)
        .options(selectinload(Ingresso.event))
        .order_by(Ingresso.data_compra.desc())
    )
    tickets = result.scalars().all()
    return tickets


@ticket_router.get("/event/{event_id}/current-price")
async def get_preco_atual(
    event_id: int,
    session: AsyncSession = Depends(get_sessao_eventos)
):
    """Retorna o preço atual do evento (do lote ativo)"""
    
    # Busca o lote ativo
    active_batch = await get_lote_ativo_para_evento(event_id, session)
    
    if not active_batch:
        # Se não há lote ativo, busca o evento para retornar o preço base
        event_result = await session.execute(select(Event).where(Event.id == event_id))
        event = event_result.scalar_one_or_none()
        
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento não encontrado"
            )
        
        return {
            "current_price": float(event.preco),
            "batch_name": "Preço base",
            "available_tickets": 0,
            "total_tickets": 0,
            "batch_number": 0
        }
    
    return {
        "current_price": float(active_batch.price),
        "batch_name": active_batch.name,
        "available_tickets": active_batch.ingressos_disponiveis,
        "total_tickets": active_batch.total_ingressos,
        "batch_number": active_batch.numero_lote,
        "progress_percentage": active_batch.porcentagem_progresso
    }
