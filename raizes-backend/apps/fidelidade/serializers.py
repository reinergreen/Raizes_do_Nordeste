from rest_framework import serializers
from .models import HistoricoPontos

class HistoricoPontosSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoPontos
        fields = ['id', 'tipo', 'pontos', 'descricao', 'pedido_id', 'criado_em']
        read_only_fields = fields

class ResgateSerializer(serializers.Serializer):
    pontos = serializers.IntegerField(min_value=1)
