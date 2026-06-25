from django.contrib import admin
from .models import Unidade

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cidade', 'ativa')
    search_fields = ('nome', 'cidade')
