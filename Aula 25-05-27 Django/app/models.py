from django.db import models

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    descricao = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    valor = models.FloatField()
    custo = models.FloatField()

    def __str__(self) -> str:
        return self.descricao

class FormaPagamento(models.Model):
    nome = models.CharField(max_length=30)
    taxa = models.FloatField()

class Venda(models.Model):
    total = models.FloatField()
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE)

class ProdutoVendido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.FloatField()
    total = models.FloatField()
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)