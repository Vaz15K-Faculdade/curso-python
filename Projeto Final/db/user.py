from typing import Optional
from datetime import date

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import select, func, update
from sqlalchemy.orm import Mapped, mapped_column
from dotenv import load_dotenv
import os

from db.database import Base, get_sessao_async

load_dotenv()


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_operator: Mapped[bool] = mapped_column(default=False, nullable=False)
    data_nascimento: Mapped[date] = mapped_column(nullable=True)
    telefone: Mapped[str] = mapped_column(nullable=True)
    cpf: Mapped[str] = mapped_column(nullable=True, unique=True)


async def get_db_usuario(session=Depends(get_sessao_async)):
    yield SQLAlchemyUserDatabase(session, User)


SECRET = os.getenv("SECRET")


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"Usuário {user.id} foi registrado.")

        # Primeiro cadastro é um superadmin
        async for session in get_sessao_async():
            result = await session.execute(select(func.count(User.id)))
            if result.scalar_one() == 1:
                await session.execute(
                    update(User).where(User.id == user.id).values(is_superuser=True)
                )
                await session.commit()
                print(f"Usuário {user.id} foi promovido a administrador.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Usuário {user.id} esqueceu a senha. Token de reset: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verificação para o usuário {user.id}. Token de verificação: {token}")


async def get_gerenciador_usuario(user_db=Depends(get_db_usuario)):
    yield UserManager(user_db)