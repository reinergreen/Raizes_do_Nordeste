from django.conf import settings
from django.db import models
from apps.unidades.models import Unidade
from apps.produtos.models import Produto

class Estoque(models.Model):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name='estoques')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='estoques')
    quantidade = models.PositiveIntegerField(default=0)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['unidade', 'produto']

    def __str__(self):
        return f'{self.unidade.nome} - {self.produto.nome}: {self.quantidade}'

class MovimentacaoEstoque(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = 'ENTRADA', 'Entrada'
        SAIDA = 'SAIDA', 'Saída'
        AJUSTE = 'AJUSTE', 'Ajuste'

    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    quantidade = models.PositiveIntegerField()
    motivo = models.CharField(max_length=200)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo} {self.quantidade} - {self.estoque}'
