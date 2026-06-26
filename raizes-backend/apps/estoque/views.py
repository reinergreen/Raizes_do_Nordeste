from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from apps.core.permissions import IsEquipeLoja, IsAdminOrGerente
from apps.core.responses import erro_regra_negocio
from apps.unidades.models import Unidade
from apps.produtos.models import Produto
from .models import Estoque, MovimentacaoEstoque
from .serializers import EstoqueSerializer, MovimentacaoEstoqueSerializer
from .services import movimentar_estoque

class EstoqueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Estoque.objects.select_related('unidade', 'produto').all().order_by('unidade_id', 'produto__nome')
    serializer_class = EstoqueSerializer
    permission_classes = [IsEquipeLoja]
    filterset_fields = ['unidade_id', 'produto_id']

    def get_queryset(self):
        qs = self.queryset
        unidade_id = self.request.query_params.get('unidadeId')
        produto_id = self.request.query_params.get('produtoId')
        if unidade_id:
            qs = qs.filter(unidade_id=unidade_id)
        if produto_id:
            qs = qs.filter(produto_id=produto_id)
        return qs

    @action(detail=False, methods=['post'], permission_classes=[IsAdminOrGerente], url_path='movimentar')
    def movimentar(self, request):
        serializer = MovimentacaoEstoqueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unidade = Unidade.objects.filter(id=serializer.validated_data['unidadeId']).first()
        produto = Produto.objects.filter(id=serializer.validated_data['produtoId']).first()
        if not unidade:
            raise NotFound('Unidade não encontrada.')
        if not produto:
            raise NotFound('Produto não encontrado.')
        try:
            mov = movimentar_estoque(
                unidade=unidade,
                produto=produto,
                tipo=serializer.validated_data['tipo'],
                quantidade=serializer.validated_data['quantidade'],
                motivo=serializer.validated_data['motivo'],
                usuario=request.user,
            )
        except ValueError:
            return erro_regra_negocio('ESTOQUE_INSUFICIENTE', 'Não há saldo suficiente para realizar a saída.', 409, path=request.path)
        return Response({'id': mov.id, 'message': 'Movimentação registrada com sucesso.'}, status=status.HTTP_201_CREATED)
