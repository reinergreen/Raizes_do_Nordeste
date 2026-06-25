from rest_framework import serializers
from .models import Unidade

class UnidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidade
        fields = ['id', 'nome', 'cidade', 'endereco', 'ativa', 'criado_em']
        read_only_fields = ['id', 'criado_em']
