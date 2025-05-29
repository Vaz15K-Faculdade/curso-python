from django.shortcuts import render

from app.models import Produto

# Create your views here.
def produto_view(request):
    produtos = Produto.objects.all()
    return render(request, "produtos.html", {"produtos": produtos})