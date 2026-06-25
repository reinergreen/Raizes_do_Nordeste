from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

from apps.core.permissions import IsAdminOrGerente
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer, LoginSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('id')
    filterset_fields = ['perfil']
    search_fields = ['nome', 'email']

    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        return UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action in ['list', 'destroy']:
            return [IsAdminOrGerente()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.perfil in ['ADMIN', 'GERENTE']:
            return self.queryset
        if user.is_authenticated:
            return Usuario.objects.filter(id=user.id)
        return Usuario.objects.none()

    @extend_schema(description='Retorna o perfil do usuário autenticado.')
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        return Response(UsuarioSerializer(request.user).data)
