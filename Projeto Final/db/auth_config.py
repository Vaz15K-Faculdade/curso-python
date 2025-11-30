"""
Configuração centralizada de autenticação para evitar duplicação de código
"""
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend, CookieTransport, JWTStrategy)
from dotenv import load_dotenv
import os
from db.user import User, get_gerenciador_usuario

load_dotenv()

SECRET = os.getenv("SECRET", "2345meia78")  # Valor padrão se não encontrar

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600, cookie_secure=False)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_gerenciador_usuario, [auth_backend])  # type: ignore

usuario_ativo = fastapi_users.current_user(active=True)
superusuario_ativo = fastapi_users.current_user(active=True, superuser=True)
