from django.contrib import admin
from .models import LogAuditoria

@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'acao', 'entidade', 'entidade_id', 'usuario', 'criado_em')
    list_filter = ('acao', 'entidade')
