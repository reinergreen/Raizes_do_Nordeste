from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError
from apps.auditoria.services import registrar_log
from apps.estoque.models import MovimentacaoEstoque
from apps.estoque.services import movimentar_estoque
from apps.produtos.models import Produto, CardapioItem
from apps.unidades.models import Unidade
from .models import Pedido, PedidoItem

STATUS_PERMITIDOS = {
    Pedido.Status.PAGO: [Pedido.Status.EM_PREPARO, Pedido.Status.CANCELADO],
    Pedido.Status.EM_PREPARO: [Pedido.Status.PRONTO, Pedido.Status.CANCELADO],
    Pedido.Status.PRONTO: [Pedido.Status.ENTREGUE, Pedido.Status.CANCELADO],
}


@transaction.atomic
def criar_pedido(cliente, unidade_id, canal_pedido, itens, usuario_log=None):
    if not canal_pedido:
        raise ValidationError({'canalPedido': 'O canal do pedido é obrigatório.'})
    if canal_pedido not in Pedido.CanalPedido.values:
        raise ValidationError({'canalPedido': 'Canal inválido. Use APP, TOTEM, BALCAO, PICKUP ou WEB.'})
    if not itens:
        raise ValidationError({'itens': 'O pedido deve possuir ao menos um item.'})

    unidade = Unidade.objects.filter(id=unidade_id, ativa=True).first()
    if not unidade:
        raise NotFound('Unidade não encontrada ou inativa.')

    pedido = Pedido.objects.create(cliente=cliente, unidade=unidade, canal_pedido=canal_pedido)
    total = Decimal('0.00')

    for item in itens:
        produto_id = item['produtoId']
        quantidade = item['quantidade']
        if quantidade <= 0:
            raise ValidationError({'quantidade': 'A quantidade deve ser maior que zero.'})

        produto = Produto.objects.filter(id=produto_id, ativo=True).first()
        if not produto:
            raise NotFound(f'Produto {produto_id} não encontrado ou inativo.')

        cardapio_item = CardapioItem.objects.filter(unidade=unidade, produto=produto, disponivel=True).first()
        if not cardapio_item:
            raise NotFound(f'Produto {produto_id} não está disponível no cardápio da unidade.')

        try:
            movimentar_estoque(unidade, produto, MovimentacaoEstoque.Tipo.SAIDA, quantidade, f'Reserva do pedido #{pedido.id}', usuario_log)
        except ValueError:
            raise ValueError('ESTOQUE_INSUFICIENTE')

        preco = cardapio_item.preco_final
        PedidoItem.objects.create(pedido=pedido, produto=produto, quantidade=quantidade, preco_unitario=preco)
        total += preco * quantidade

    pedido.total = total
    pedido.save(update_fields=['total', 'atualizado_em'])
    registrar_log(usuario_log, 'CRIACAO_PEDIDO', 'Pedido', pedido.id, {
        'clienteId': cliente.id,
        'unidadeId': unidade.id,
        'canalPedido': canal_pedido,
        'total': str(total),
    })
    return pedido


@transaction.atomic
def atualizar_status_pedido(pedido, novo_status, usuario):
    if novo_status not in Pedido.Status.values:
        raise ValidationError({'status': 'Status inválido.'})

    permitidos = STATUS_PERMITIDOS.get(pedido.status, [])
    if novo_status not in permitidos:
        raise ValueError('STATUS_INVALIDO')

    status_anterior = pedido.status
    pedido.status = novo_status
    pedido.save(update_fields=['status', 'atualizado_em'])
    registrar_log(usuario, 'ATUALIZACAO_STATUS_PEDIDO', 'Pedido', pedido.id, {
        'statusAnterior': status_anterior,
        'statusNovo': novo_status,
    })
    return pedido


@transaction.atomic
def cancelar_pedido(pedido, usuario):
    if pedido.status in [Pedido.Status.ENTREGUE, Pedido.Status.CANCELADO]:
        raise ValueError('CANCELAMENTO_INVALIDO')
    status_anterior = pedido.status
    pedido.status = Pedido.Status.CANCELADO
    pedido.save(update_fields=['status', 'atualizado_em'])
    for item in pedido.itens.select_related('produto'):
        movimentar_estoque(pedido.unidade, item.produto, MovimentacaoEstoque.Tipo.ENTRADA, item.quantidade, f'Estorno do pedido #{pedido.id}', usuario)
    registrar_log(usuario, 'CANCELAMENTO_PEDIDO', 'Pedido', pedido.id, {'statusAnterior': status_anterior})
    return pedido
