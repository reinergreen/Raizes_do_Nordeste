from decimal import Decimal
from django.conf import settings
from django.db import models
from apps.unidades.models import Unidade
from apps.produtos.models import Produto

class Pedido(models.Model):
    class CanalPedido(models.TextChoices):
        APP = 'APP', 'App'
        TOTEM = 'TOTEM', 'Totem'
        BALCAO = 'BALCAO', 'Balcão'
        PICKUP = 'PICKUP', 'Pickup'
        WEB = 'WEB', 'Web'

    class Status(models.TextChoices):
        AGUARDANDO_PAGAMENTO = 'AGUARDANDO_PAGAMENTO', 'Aguardando pagamento'
        PAGO = 'PAGO', 'Pago'
        EM_PREPARO = 'EM_PREPARO', 'Em preparo'
        PRONTO = 'PRONTO', 'Pronto'
        ENTREGUE = 'ENTREGUE', 'Entregue'
        CANCELADO = 'CANCELADO', 'Cancelado'
        PAGAMENTO_RECUSADO = 'PAGAMENTO_RECUSADO', 'Pagamento recusado'

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pedidos')
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name='pedidos')
    canal_pedido = models.CharField(max_length=20, choices=CanalPedido.choices)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.AGUARDANDO_PAGAMENTO)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Pedido #{self.id} - {self.status}'

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'
