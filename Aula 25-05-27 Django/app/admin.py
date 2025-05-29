from django.contrib import admin

from app.models import Categoria, Produto, Venda, FormaPagamento, ProdutoVendido

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("descricao", "categoria", "custo", "valor")

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")

class VendaAdmin(admin.ModelAdmin):
    list_display = ("total", "forma_pagamento")

class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "taxa")

class ProdutoVendidoAdmin(admin.ModelAdmin):
    list_display = ("venda", "produto", "quantidade", "total")

# Register your models here.
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Venda, VendaAdmin)
admin.site.register(FormaPagamento, FormaPagamentoAdmin)
admin.site.register(ProdutoVendido, ProdutoVendidoAdmin)