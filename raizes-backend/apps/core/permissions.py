from rest_framework.permissions import BasePermission


class PerfilPermission(BasePermission):
    perfis_permitidos = []

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            (request.user.is_superuser or request.user.perfil in self.perfis_permitidos)
        )


class IsAdminOrGerente(PerfilPermission):
    perfis_permitidos = ['ADMIN', 'GERENTE']


class IsEquipeLoja(PerfilPermission):
    perfis_permitidos = ['ADMIN', 'GERENTE', 'ATENDENTE', 'COZINHA']


class IsCozinhaOuGerencia(PerfilPermission):
    perfis_permitidos = ['ADMIN', 'GERENTE', 'COZINHA']


class IsCliente(PerfilPermission):
    perfis_permitidos = ['CLIENTE']
