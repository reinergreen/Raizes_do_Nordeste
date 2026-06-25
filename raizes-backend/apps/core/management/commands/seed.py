from django.core.management.base import BaseCommand
from apps.usuarios.models import Usuario
from apps.unidades.models import Unidade
from apps.produtos.models import Produto, CardapioItem
from apps.estoque.models import Estoque

class Command(BaseCommand):
    help = 'Cria dados iniciais para testar a API.'

    def handle(self, *args, **options):
        usuarios = [
            ('admin@raizes.com', 'Admin@123', 'Administrador', 'ADMIN', True, True),
            ('gerente@raizes.com', 'Gerente@123', 'Gerente Recife', 'GERENTE', True, False),
            ('atendente@raizes.com', 'Atendente@123', 'Atendente Balcão', 'ATENDENTE', True, False),
            ('cozinha@raizes.com', 'Cozinha@123', 'Equipe Cozinha', 'COZINHA', True, False),
            ('cliente@exemplo.com', 'Cliente@123', 'Maria Cliente', 'CLIENTE', False, False),
        ]
        for email, senha, nome, perfil, staff, superuser in usuarios:
            if not Usuario.objects.filter(email=email).exists():
                Usuario.objects.create_user(email=email, password=senha, nome=nome, perfil=perfil, is_staff=staff, is_superuser=superuser, consentimento_fidelidade=True)

        unidade, _ = Unidade.objects.get_or_create(nome='Raízes Recife Centro', defaults={'cidade': 'Recife', 'endereco': 'Rua das Mangueiras, 100', 'ativa': True})
        unidade2, _ = Unidade.objects.get_or_create(nome='Raízes Salvador Pituba', defaults={'cidade': 'Salvador', 'endereco': 'Av. Atlântica, 55', 'ativa': True})

        produtos = [
            ('Cuscuz Nordestino', 'Cuscuz com queijo coalho e manteiga de garrafa.', 'Pratos', '18.90', 80),
            ('Baião de Dois', 'Arroz, feijão verde, queijo coalho e carne de sol.', 'Pratos', '32.90', 40),
            ('Tapioca de Carne de Sol', 'Tapioca recheada com carne de sol e queijo.', 'Lanches', '24.90', 50),
            ('Suco de Cajá', 'Suco natural de cajá.', 'Bebidas', '9.90', 100),
        ]
        for nome, desc, cat, preco, qtd in produtos:
            produto, _ = Produto.objects.get_or_create(nome=nome, defaults={'descricao': desc, 'categoria': cat, 'preco': preco, 'ativo': True})
            for uni in [unidade, unidade2]:
                CardapioItem.objects.get_or_create(unidade=uni, produto=produto, defaults={'disponivel': True})
                Estoque.objects.get_or_create(unidade=uni, produto=produto, defaults={'quantidade': qtd})

        self.stdout.write(self.style.SUCCESS('Seed executado com sucesso.'))
        self.stdout.write('Usuário de teste: cliente@exemplo.com / Cliente@123')
        self.stdout.write('Admin: admin@raizes.com / Admin@123')
