from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.responses import erro_regra_negocio
from .models import HistoricoPontos
from .serializers import HistoricoPontosSerializer, ResgateSerializer
from .services import saldo_pontos, resgatar_pontos

class FidelidadeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HistoricoPontosSerializer

    def get_queryset(self):
        return HistoricoPontos.objects.filter(usuario=self.request.user)

    @action(detail=False, methods=['get'], url_path='saldo')
    def saldo(self, request):
        return Response({
            'usuarioId': request.user.id,
            'consentimento': request.user.consentimento_fidelidade,
            'saldo': saldo_pontos(request.user),
        })

    @action(detail=False, methods=['post'], url_path='resgatar')
    def resgatar(self, request):
        serializer = ResgateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            hist = resgatar_pontos(request.user, serializer.validated_data['pontos'], request.user)
        except ValueError as exc:
            if str(exc) == 'SALDO_INSUFICIENTE':
                return erro_regra_negocio('SALDO_INSUFICIENTE', 'Saldo de pontos insuficiente para o resgate.', 409, path=request.path)
            return erro_regra_negocio('PONTOS_INVALIDOS', 'Quantidade de pontos inválida.', 422, path=request.path)
        return Response(HistoricoPontosSerializer(hist).data, status=201)
