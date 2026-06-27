from rest_framework import serializers
from .models import LogAuditoria

class LogAuditoriaSerializer(serializers.ModelSerializer):
    usuarioEmail = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = LogAuditoria
        fields = ['id', 'usuarioEmail', 'acao', 'entidade', 'entidade_id', 'detalhes', 'criado_em']
        read_only_fields = fields
