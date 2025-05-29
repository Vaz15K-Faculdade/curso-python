from django.shortcuts import render

from app.models import Produto, Venda

def home_view(request):
    return render(
        request, 
        'home.html', 
        {
            'paginas': [
                {'nome': 'Vendas', 'url': '/vendas'},
                {'nome': 'Produtos', 'url': '/produtos'},
                # {'nome': 'Formas de Pagamento', 'url': '/formasPagamento'},
                # {'nome': 'Categorias', 'url': '/categorias'},
            ]
        }
    )

# Create your views here.
def produtos_view(request):
    # equivalente ao "SELECT * FROM Produto"
    produtos = Produto.objects.all()
    
    return render(request, 'produtos.html', {'produtos': produtos})

def vendas_view(request):
    vendas = Venda.objects.prefetch_related('produtos_vendidos__produto')
    # vendas = Venda.objects.all()

    return render(request, 'vendas.html', {'vendas': vendas})
