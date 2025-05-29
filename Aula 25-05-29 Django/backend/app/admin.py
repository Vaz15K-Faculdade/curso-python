from django.contrib import admin

from app.models import Produto, Categoria, FormaDePagamento, Venda, ProdutoVendido

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'categoria', 'custo', 'valor')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')

class FormaDePagamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'taxa')

class VendaAdmin(admin.ModelAdmin):
    list_display = ('horario', 'total', 'formaDePagamento')

class ProdutoVendidoAdmin(admin.ModelAdmin):
    list_display = ('venda', 'produto', 'quantidade', 'total')

# Register your models here.
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(FormaDePagamento, FormaDePagamentoAdmin)
admin.site.register(Venda, VendaAdmin)
admin.site.register(ProdutoVendido, ProdutoVendidoAdmin)