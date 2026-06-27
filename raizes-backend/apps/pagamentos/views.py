from apps.core.responses import erro_regra_negocio
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PagamentoMockInputSerializer, PagamentoSerializer
from .services import solicitar_pagamento_mock


class PagamentoMockView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=PagamentoMockInputSerializer,
        responses={201: PagamentoSerializer}
    )
    def post(self, request):
        serializer = PagamentoMockInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pagamento = solicitar_pagamento_mock(
                pedido_id=serializer.validated_data['pedidoId'],
                forma=serializer.validated_data['formaPagamento'],
                usuario=request.user,
                forcar_status=serializer.validated_data.get('forcarStatus'),
            )
        except ValueError:
            return erro_regra_negocio(
                'PAGAMENTO_NAO_PERMITIDO',
                'O pedido não está em um status que permita pagamento.',
                409,
                path=request.path
            )
        return Response(PagamentoSerializer(pagamento).data, status=201)
