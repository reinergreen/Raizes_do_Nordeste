from django.db import models

class Unidade(models.Model):
    nome = models.CharField(max_length=120)
    cidade = models.CharField(max_length=80)
    endereco = models.CharField(max_length=200)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.cidade}'
