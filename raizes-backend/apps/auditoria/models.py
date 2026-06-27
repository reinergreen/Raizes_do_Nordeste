from django.conf import settings
from django.db import models

class LogAuditoria(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    acao = models.CharField(max_length=80)
    entidade = models.CharField(max_length=80)
    entidade_id = models.CharField(max_length=40, blank=True)
    detalhes = models.JSONField(default=dict, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.acao} em {self.entidade} #{self.entidade_id}'
