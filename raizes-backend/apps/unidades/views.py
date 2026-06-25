from rest_framework import viewsets, permissions
from apps.core.permissions import IsAdminOrGerente
from .models import Unidade
from .serializers import UnidadeSerializer

class UnidadeViewSet(viewsets.ModelViewSet):
    queryset = Unidade.objects.all().order_by('nome')
    serializer_class = UnidadeSerializer
    filterset_fields = ['ativa', 'cidade']
    search_fields = ['nome', 'cidade']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrGerente()]
