import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ninja import NinjaAPI
from app.models import Produto, Categoria, FormaDePagamento, Venda, ProdutoVendido
from app.schemas import ProdutoJson, CategoriaJson, FormaDePagamentoJson, VendaJson

api = NinjaAPI()

@api.get("/teste")
def get_teste(request):
    return {"message": "Hello, World!"}

@api.get("/produtos", response=list[ProdutoJson])
def get_produtos(request):
    produtos = Produto.objects.all()
    return produtos

@api.get("/categorias", response=list[CategoriaJson])
def get_categorias(request):
    categorias = Categoria.objects.all()
    return categorias

@api.get("/formas-de-pagamento", response=list[FormaDePagamentoJson])
def get_formas_de_pagamento(request):
    formas_de_pagamento = FormaDePagamento.objects.all()
    return formas_de_pagamento

@api.get("/vendas", response=list[VendaJson])
def get_vendas(request):
    vendas = Venda.objects.all()
    return vendas