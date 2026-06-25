from django.contrib import admin
from .models import Produto, CardapioItem

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'categoria', 'preco', 'ativo')
    search_fields = ('nome', 'descricao')

@admin.register(CardapioItem)
class CardapioItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'unidade', 'produto', 'preco_final', 'disponivel')
    list_filter = ('unidade', 'disponivel')
