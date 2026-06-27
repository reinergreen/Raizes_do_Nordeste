from django.contrib import admin
from .models import HistoricoPontos

@admin.register(HistoricoPontos)
class HistoricoPontosAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'tipo', 'pontos', 'pedido_id', 'criado_em')
    list_filter = ('tipo',)
