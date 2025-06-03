import requests

HOST_BACKEND = "http://localhost:8000"

def get_backend_data(endpoint):
    url = HOST_BACKEND + endpoint
    respose = requests.get(url)

    return respose.json()

def get_produtos():
    return get_backend_data("/api/produtos")

def get_categorias():
    return get_backend_data("/api/categorias")

def get_formas_de_pagamento():
    return get_backend_data("/api/formas-de-pagamento")

def get_vendas():
    return get_backend_data("/api/vendas")