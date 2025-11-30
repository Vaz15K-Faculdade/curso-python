import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
ASSETS_DIR = FRONTEND_DIR / "assets"
COMPONENTS_DIR = FRONTEND_DIR / "components"

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

WINDOW_TITLE = "Toten Virtual - Sistema de Ingressos"
WINDOW_SIZE = (1200, 800)
WINDOW_MIN_SIZE = (800, 600)

COLORS = {
    "primary": "#3498db",
    "primary_dark": "#2980b9",
    "primary_darker": "#21618c",
    "secondary": "#e74c3c",
    "secondary_dark": "#c0392b",
    "success": "#27ae60",
    "warning": "#f39c12",
    "danger": "#e74c3c",
    "dark": "#2c3e50",
    "light": "#ecf0f1",
    "white": "#ffffff",
    "gray": "#7f8c8d",
    "gray_light": "#bdc3c7"
}

FONTS = {
    "title": {"family": "Segoe UI", "size": 24, "bold": True},
    "subtitle": {"family": "Segoe UI", "size": 18, "bold": True},
    "header": {"family": "Segoe UI", "size": 16, "bold": True},
    "body": {"family": "Segoe UI", "size": 12, "bold": False},
    "small": {"family": "Segoe UI", "size": 10, "bold": False}
}

GRID_CONFIG = {
    "max_columns": 3,
    "card_spacing": 20,
    "margin": 20
}

MESSAGES = {
    "loading_events": "Carregando eventos...",
    "loading_tickets": "Carregando ingressos...",
    "no_events": "Nenhum evento disponível no momento.",
    "no_tickets": "Você ainda não possui ingressos.\nVisite o catálogo para comprar!",
    "login_success": "Login realizado com sucesso!",
    "logout_success": "Logout realizado com sucesso!",
    "register_success": "Cadastro realizado com sucesso! Você pode fazer login agora.",
    "purchase_success": "Ingresso comprado com sucesso!\nVocê pode visualizá-lo em 'Meus Ingressos'."
}

VALIDATION = {
    "min_password_length": 6,
    "cpf_length": 11,
    "email_pattern": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
}
