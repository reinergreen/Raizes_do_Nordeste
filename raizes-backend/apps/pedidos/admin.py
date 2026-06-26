from django.contrib import admin
from .models import Pedido, PedidoItem

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'unidade', 'canal_pedido', 'status', 'total', 'criado_em')
    list_filter = ('status', 'canal_pedido', 'unidade')
    inlines = [PedidoItemInline]
