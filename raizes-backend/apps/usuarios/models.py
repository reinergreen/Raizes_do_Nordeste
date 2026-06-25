from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('perfil', Usuario.Perfil.ADMIN)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    class Perfil(models.TextChoices):
        CLIENTE = 'CLIENTE', 'Cliente'
        ATENDENTE = 'ATENDENTE', 'Atendente'
        COZINHA = 'COZINHA', 'Cozinha'
        GERENTE = 'GERENTE', 'Gerente'
        ADMIN = 'ADMIN', 'Administrador'

    username = models.CharField(max_length=150, unique=True, blank=True)
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=150)
    perfil = models.CharField(max_length=20, choices=Perfil.choices, default=Perfil.CLIENTE)
    telefone = models.CharField(max_length=20, blank=True)
    consentimento_fidelidade = models.BooleanField(default=False)
    data_consentimento_fidelidade = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']
    objects = UsuarioManager()

    def save(self, *args, **kwargs):
        if self.email and not self.username:
            self.username = self.email
        if self.consentimento_fidelidade and not self.data_consentimento_fidelidade:
            self.data_consentimento_fidelidade = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome} ({self.perfil})'
