from rest_framework import serializers
from .models import Produto, CardapioItem

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'categoria', 'preco', 'ativo', 'criado_em']
        read_only_fields = ['id', 'criado_em']

class CardapioItemSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    produtoId = serializers.IntegerField(source='produto_id', write_only=True)
    unidadeId = serializers.IntegerField(source='unidade_id')
    precoFinal = serializers.DecimalField(source='preco_final', max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = CardapioItem
        fields = ['id', 'unidadeId', 'produto', 'produtoId', 'preco_override', 'precoFinal', 'disponivel']
        read_only_fields = ['id']
