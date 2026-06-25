from rest_framework import viewsets, permissions
from apps.core.permissions import IsAdminOrGerente
from .models import Produto, CardapioItem
from .serializers import ProdutoSerializer, CardapioItemSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all().order_by('nome')
    serializer_class = ProdutoSerializer
    filterset_fields = ['ativo', 'categoria']
    search_fields = ['nome', 'descricao']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrGerente()]

class CardapioItemViewSet(viewsets.ModelViewSet):
    queryset = CardapioItem.objects.select_related('produto', 'unidade').all().order_by('unidade_id', 'produto__nome')
    serializer_class = CardapioItemSerializer
    filterset_fields = ['unidade_id', 'disponivel']
    search_fields = ['produto__nome', 'produto__descricao']

    def get_queryset(self):
        qs = self.queryset
        unidade_id = self.request.query_params.get('unidadeId')
        if unidade_id:
            qs = qs.filter(unidade_id=unidade_id)
        return qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrGerente()]
