from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.permissions import IsEquipeLoja, IsCozinhaOuGerencia
from apps.core.responses import erro_regra_negocio
from .models import Pedido
from .serializers import PedidoSerializer, PedidoCreateSerializer, PedidoStatusSerializer
from .services import criar_pedido, atualizar_status_pedido, cancelar_pedido

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.select_related('cliente', 'unidade').prefetch_related('itens__produto').all().order_by('-criado_em')
    serializer_class = PedidoSerializer
    filterset_fields = ['status', 'canal_pedido', 'unidade_id']
    ordering_fields = ['criado_em', 'total']

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        if self.action in ['atualizar_status']:
            return [IsCozinhaOuGerencia()]
        if self.action in ['cancelar']:
            return [permissions.IsAuthenticated()]
        return [IsEquipeLoja()]

    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        canal = self.request.query_params.get('canalPedido')
        if canal:
            qs = qs.filter(canal_pedido=canal)
        if user.is_authenticated and user.perfil == 'CLIENTE':
            qs = qs.filter(cliente=user)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = PedidoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pedido = criar_pedido(
                cliente=request.user,
                unidade_id=serializer.validated_data['unidadeId'],
                canal_pedido=serializer.validated_data['canalPedido'],
                itens=serializer.validated_data['itens'],
                usuario_log=request.user,
            )
        except ValueError:
            return erro_regra_negocio('ESTOQUE_INSUFICIENTE', 'Não há quantidade suficiente para um ou mais itens.', 409, path=request.path)
        return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='status')
    def atualizar_status(self, request, pk=None):
        pedido = self.get_object()
        serializer = PedidoStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pedido = atualizar_status_pedido(pedido, serializer.validated_data['status'], request.user)
        except ValueError:
            return erro_regra_negocio('STATUS_INVALIDO', 'Transição de status não permitida para o estado atual do pedido.', 409, path=request.path)
        return Response(PedidoSerializer(pedido).data)

    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        pedido = self.get_object()
        if request.user.perfil == 'CLIENTE' and pedido.cliente_id != request.user.id:
            return erro_regra_negocio('SEM_PERMISSAO', 'Cliente só pode cancelar o próprio pedido.', 403, path=request.path)
        try:
            pedido = cancelar_pedido(pedido, request.user)
        except ValueError:
            return erro_regra_negocio('CANCELAMENTO_INVALIDO', 'Pedido entregue ou já cancelado não pode ser cancelado.', 409, path=request.path)
        return Response(PedidoSerializer(pedido).data)
