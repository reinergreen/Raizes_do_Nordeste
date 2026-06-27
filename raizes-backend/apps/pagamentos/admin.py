from django.contrib import admin
from .models import Pagamento

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'forma', 'status', 'transacao_id', 'criado_em')
    list_filter = ('status', 'forma')
