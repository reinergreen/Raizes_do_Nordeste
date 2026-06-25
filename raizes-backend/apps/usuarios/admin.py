from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('id', 'nome', 'email', 'perfil', 'is_active')
    list_filter = ('perfil', 'is_active')
    search_fields = ('nome', 'email')
    ordering = ('id',)
    fieldsets = UserAdmin.fieldsets + (
        ('Dados do sistema', {'fields': ('nome', 'perfil', 'telefone', 'consentimento_fidelidade', 'data_consentimento_fidelidade')}),
    )
