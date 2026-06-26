from rest_framework import serializers
from .models import Pedido, PedidoItem

class PedidoItemSerializer(serializers.ModelSerializer):
    produtoId = serializers.IntegerField(source='produto_id', read_only=True)
    produtoNome = serializers.CharField(source='produto.nome', read_only=True)
    precoUnitario = serializers.DecimalField(source='preco_unitario', max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = PedidoItem
        fields = ['id', 'produtoId', 'produtoNome', 'quantidade', 'precoUnitario', 'subtotal']

class PedidoSerializer(serializers.ModelSerializer):
    clienteId = serializers.IntegerField(source='cliente_id', read_only=True)
    clienteNome = serializers.CharField(source='cliente.nome', read_only=True)
    unidadeId = serializers.IntegerField(source='unidade_id', read_only=True)
    unidadeNome = serializers.CharField(source='unidade.nome', read_only=True)
    canalPedido = serializers.CharField(source='canal_pedido')
    itens = PedidoItemSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'clienteId', 'clienteNome', 'unidadeId', 'unidadeNome', 'canalPedido', 'status', 'total', 'itens', 'criado_em', 'atualizado_em']
        read_only_fields = fields

class ItemPedidoInputSerializer(serializers.Serializer):
    produtoId = serializers.IntegerField()
    quantidade = serializers.IntegerField(min_value=1)

class PedidoCreateSerializer(serializers.Serializer):
    unidadeId = serializers.IntegerField()
    canalPedido = serializers.ChoiceField(choices=Pedido.CanalPedido.choices)
    itens = ItemPedidoInputSerializer(many=True)
    formaPagamento = serializers.CharField(default='MOCK')

class PedidoStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Pedido.Status.choices)
