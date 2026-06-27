from django.db import transaction
from apps.auditoria.services import registrar_log
from .models import HistoricoPontos


def saldo_pontos(usuario):
    saldo = 0
    for item in usuario.historico_pontos.all():
        saldo += item.pontos if item.tipo == HistoricoPontos.Tipo.CREDITO else -item.pontos
    return saldo


@transaction.atomic
def creditar_pontos_pedido(pedido, usuario_log=None):
    cliente = pedido.cliente
    if not cliente.consentimento_fidelidade:
        return None
    pontos = int(pedido.total // 10)
    if pontos <= 0:
        return None
    hist = HistoricoPontos.objects.create(
        usuario=cliente,
        tipo=HistoricoPontos.Tipo.CREDITO,
        pontos=pontos,
        descricao=f'Pontos gerados pelo pedido #{pedido.id}',
        pedido_id=pedido.id,
    )
    registrar_log(usuario_log, 'CREDITO_FIDELIDADE', 'HistoricoPontos', hist.id, {'clienteId': cliente.id, 'pontos': pontos})
    return hist


@transaction.atomic
def resgatar_pontos(usuario, pontos, usuario_log=None):
    if pontos <= 0:
        raise ValueError('PONTOS_INVALIDOS')
    atual = saldo_pontos(usuario)
    if atual < pontos:
        raise ValueError('SALDO_INSUFICIENTE')
    hist = HistoricoPontos.objects.create(
        usuario=usuario,
        tipo=HistoricoPontos.Tipo.RESGATE,
        pontos=pontos,
        descricao='Resgate simples de pontos de fidelidade',
    )
    registrar_log(usuario_log, 'RESGATE_FIDELIDADE', 'HistoricoPontos', hist.id, {'clienteId': usuario.id, 'pontos': pontos})
    return hist
