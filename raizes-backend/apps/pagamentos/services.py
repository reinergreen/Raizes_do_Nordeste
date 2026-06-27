from django.db import transaction
from rest_framework.exceptions import NotFound
from apps.auditoria.services import registrar_log
from apps.pedidos.models import Pedido
from apps.fidelidade.services import creditar_pontos_pedido
from .models import Pagamento


@transaction.atomic
def solicitar_pagamento_mock(pedido_id, forma, usuario, forcar_status=None):
    pedido = Pedido.objects.select_for_update().filter(id=pedido_id).first()
    if not pedido:
        raise NotFound('Pedido não encontrado.')
    if getattr(usuario, 'perfil', None) == 'CLIENTE' and pedido.cliente_id != usuario.id:
        raise ValueError('PAGAMENTO_NAO_PERMITIDO')
    if pedido.status not in [Pedido.Status.AGUARDANDO_PAGAMENTO, Pedido.Status.PAGAMENTO_RECUSADO]:
        raise ValueError('PAGAMENTO_NAO_PERMITIDO')

    status_final = forcar_status or Pagamento.Status.APROVADO
    if status_final not in Pagamento.Status.values:
        status_final = Pagamento.Status.RECUSADO

    pagamento = Pagamento.objects.create(
        pedido=pedido,
        forma=forma,
        status=status_final,
        payload_retorno={
            'gateway': 'mock-raizes',
            'mensagem': 'Pagamento aprovado no ambiente simulado.' if status_final == Pagamento.Status.APROVADO else 'Pagamento recusado no ambiente simulado.',
            'valor': str(pedido.total),
        }
    )

    status_anterior = pedido.status
    if status_final == Pagamento.Status.APROVADO:
        pedido.status = Pedido.Status.PAGO
        pedido.save(update_fields=['status', 'atualizado_em'])
        creditar_pontos_pedido(pedido, usuario)
    else:
        pedido.status = Pedido.Status.PAGAMENTO_RECUSADO
        pedido.save(update_fields=['status', 'atualizado_em'])

    registrar_log(usuario, 'PAGAMENTO_MOCK', 'Pagamento', pagamento.id, {
        'pedidoId': pedido.id,
        'statusAnteriorPedido': status_anterior,
        'statusPagamento': status_final,
        'transacaoId': str(pagamento.transacao_id),
    })
    return pagamento
