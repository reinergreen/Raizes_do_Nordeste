from decimal import Decimal
from django.db import models
from apps.unidades.models import Unidade


class Produto(models.Model):
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    categoria = models.CharField(max_length=60, default='Lanches')
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class CardapioItem(models.Model):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name='cardapio')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='cardapios')
    preco_override = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    disponivel = models.BooleanField(default=True)

    class Meta:
        unique_together = ['unidade', 'produto']

    @property
    def preco_final(self):
        return self.preco_override if self.preco_override is not None else self.produto.preco

    def __str__(self):
        return f'{self.produto.nome} - {self.unidade.nome}'
