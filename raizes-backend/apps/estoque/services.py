from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.auditoria.services import registrar_log
from .models import Estoque, MovimentacaoEstoque


@transaction.atomic
def movimentar_estoque(unidade, produto, tipo, quantidade, motivo, usuario=None):
    if quantidade <= 0:
        raise ValidationError({'quantidade': 'A quantidade deve ser maior que zero.'})

    estoque, _ = Estoque.objects.select_for_update().get_or_create(
        unidade=unidade, produto=produto, defaults={'quantidade': 0}
    )

    if tipo == MovimentacaoEstoque.Tipo.SAIDA:
        if estoque.quantidade < quantidade:
            raise ValueError('ESTOQUE_INSUFICIENTE')
        estoque.quantidade -= quantidade
    elif tipo == MovimentacaoEstoque.Tipo.ENTRADA:
        estoque.quantidade += quantidade
    elif tipo == MovimentacaoEstoque.Tipo.AJUSTE:
        estoque.quantidade = quantidade
    else:
        raise ValidationError({'tipo': 'Tipo de movimentação inválido.'})

    estoque.save(update_fields=['quantidade', 'atualizado_em'])
    mov = MovimentacaoEstoque.objects.create(
        estoque=estoque, tipo=tipo, quantidade=quantidade, motivo=motivo, usuario=usuario
    )
    registrar_log(usuario, 'MOVIMENTACAO_ESTOQUE', 'Estoque', estoque.id, {
        'produtoId': produto.id,
        'unidadeId': unidade.id,
        'tipo': tipo,
        'quantidade': quantidade,
        'saldoAtual': estoque.quantidade,
    })
    return mov


def verificar_saldo(unidade, produto, quantidade):
    estoque = Estoque.objects.filter(unidade=unidade, produto=produto).first()
    return estoque is not None and estoque.quantidade >= quantidade
