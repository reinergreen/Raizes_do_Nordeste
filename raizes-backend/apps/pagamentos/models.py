import uuid
from django.db import models
from apps.pedidos.models import Pedido

class Pagamento(models.Model):
    class Forma(models.TextChoices):
        MOCK = 'MOCK', 'Mock'
        PIX = 'PIX', 'Pix simulado'
        CARTAO = 'CARTAO', 'Cartão simulado'

    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        APROVADO = 'APROVADO', 'Aprovado'
        RECUSADO = 'RECUSADO', 'Recusado'

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='pagamentos')
    forma = models.CharField(max_length=20, choices=Forma.choices, default=Forma.MOCK)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    transacao_id = models.UUIDField(default=uuid.uuid4, editable=False)
    payload_retorno = models.JSONField(default=dict, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pagamento {self.status} - Pedido #{self.pedido_id}'
