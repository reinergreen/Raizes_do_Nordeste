from django.contrib import admin
from .models import Estoque, MovimentacaoEstoque

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'unidade', 'produto', 'quantidade', 'atualizado_em')
    list_filter = ('unidade',)

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'estoque', 'tipo', 'quantidade', 'usuario', 'criado_em')
    list_filter = ('tipo', 'criado_em')
