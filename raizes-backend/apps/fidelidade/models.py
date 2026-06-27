from django.conf import settings
from django.db import models

class HistoricoPontos(models.Model):
    class Tipo(models.TextChoices):
        CREDITO = 'CREDITO', 'Crédito'
        RESGATE = 'RESGATE', 'Resgate'

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='historico_pontos')
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    pontos = models.IntegerField()
    descricao = models.CharField(max_length=200)
    pedido_id = models.IntegerField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
