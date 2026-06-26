from rest_framework import serializers
from apps.produtos.serializers import ProdutoSerializer
from apps.unidades.serializers import UnidadeSerializer
from .models import Estoque, MovimentacaoEstoque

class EstoqueSerializer(serializers.ModelSerializer):
    unidade = UnidadeSerializer(read_only=True)
    produto = ProdutoSerializer(read_only=True)
    unidadeId = serializers.IntegerField(source='unidade_id', read_only=True)
    produtoId = serializers.IntegerField(source='produto_id', read_only=True)

    class Meta:
        model = Estoque
        fields = ['id', 'unidadeId', 'produtoId', 'unidade', 'produto', 'quantidade', 'atualizado_em']
        read_only_fields = fields

class MovimentacaoEstoqueSerializer(serializers.Serializer):
    unidadeId = serializers.IntegerField()
    produtoId = serializers.IntegerField()
    tipo = serializers.ChoiceField(choices=MovimentacaoEstoque.Tipo.choices)
    quantidade = serializers.IntegerField(min_value=1)
    motivo = serializers.CharField(max_length=200)
