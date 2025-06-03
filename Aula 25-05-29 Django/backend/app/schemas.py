from app.models import Produto, Categoria, FormaDePagamento, Venda, ProdutoVendido
from ninja import ModelSchema

class ProdutoJson(ModelSchema):
    class Meta:
        model = Produto
        fields = "__all__"

class CategoriaJson(ModelSchema):
    class Meta:
        model = Categoria
        fields = "__all__"

class FormaDePagamentoJson(ModelSchema):
    class Meta:
        model = FormaDePagamento
        fields = "__all__"

class ProdutoVendidoJson(ModelSchema):
    class Meta:
        model = ProdutoVendido
        fields = "__all__"

class VendaJson(ModelSchema):
    produtos_vendidos: list[ProdutoVendidoJson] 
    class Meta:
        model = Venda
        fields = "__all__"
