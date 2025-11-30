from fastapi import APIRouter, Depends
from db.user import User, get_db_usuario
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from datetime import date
from sqlalchemy import select
from fastapi_users.db import SQLAlchemyUserDatabase
from typing import List
from db.event_routes import event_router
from db.ticket_routes import ticket_router
from db.auth_config import fastapi_users, superusuario_ativo, auth_backend

class UserRead(BaseUser[int]):
    is_operator: bool
    data_nascimento: date | None
    telefone: str | None
    cpf: str | None

class UserCreate(BaseUserCreate):
    is_operator: bool
    data_nascimento: date | None
    telefone: str | None
    cpf: str | None

class UserUpdate(BaseUserUpdate):
    is_operator: bool
    data_nascimento: date | None
    telefone: str | None
    cpf: str | None

router = APIRouter()

# Rota personalizada para listar todos os usuários
@router.get("/users/", response_model=List[UserRead])
async def get_todos_usuarios(
    user_db: SQLAlchemyUserDatabase = Depends(get_db_usuario),
    current_user: User = Depends(superusuario_ativo)
):
    """Lista todos os usuários (apenas para superusuários)"""
    async with user_db.session as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users

@router.get("/admin/dashboard")
def painel_admin(user: User = Depends(superusuario_ativo)):
    return {"message": f"Bem Vindo, admin {user.email}!"}

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Incluir rotas de eventos
router.include_router(event_router)

# Incluir rotas de tickets
router.include_router(ticket_router)