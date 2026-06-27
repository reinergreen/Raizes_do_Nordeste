from rest_framework import viewsets
from apps.core.permissions import IsAdminOrGerente
from .models import LogAuditoria
from .serializers import LogAuditoriaSerializer

class LogAuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogAuditoria.objects.select_related('usuario').all()
    serializer_class = LogAuditoriaSerializer
    permission_classes = [IsAdminOrGerente]
    filterset_fields = ['acao', 'entidade', 'entidade_id']
    search_fields = ['acao', 'entidade']
