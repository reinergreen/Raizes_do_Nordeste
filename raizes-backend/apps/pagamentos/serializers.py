from rest_framework import serializers
from .models import Pagamento

class PagamentoMockInputSerializer(serializers.Serializer):
    pedidoId = serializers.IntegerField()
    formaPagamento = serializers.ChoiceField(choices=Pagamento.Forma.choices, default=Pagamento.Forma.MOCK)
    forcarStatus = serializers.ChoiceField(choices=Pagamento.Status.choices, required=False)

class PagamentoSerializer(serializers.ModelSerializer):
    pedidoId = serializers.IntegerField(source='pedido_id', read_only=True)
    transacaoId = serializers.UUIDField(source='transacao_id', read_only=True)
    payloadRetorno = serializers.JSONField(source='payload_retorno', read_only=True)

    class Meta:
        model = Pagamento
        fields = ['id', 'pedidoId', 'forma', 'status', 'transacaoId', 'payloadRetorno', 'criado_em']
        read_only_fields = fields
