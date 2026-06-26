from django.test import TestCase
from apps.core.management.commands.seed import Command
from apps.usuarios.models import Usuario
from apps.unidades.models import Unidade
from apps.produtos.models import Produto
from apps.pedidos.services import criar_pedido
from apps.pedidos.models import Pedido

class PedidoServiceTest(TestCase):
    def setUp(self):
        Command().handle()
        self.cliente = Usuario.objects.get(email='cliente@exemplo.com')
        self.unidade = Unidade.objects.first()
        self.produto = Produto.objects.first()

    def test_criar_pedido_com_estoque(self):
        pedido = criar_pedido(self.cliente, self.unidade.id, 'APP', [{'produtoId': self.produto.id, 'quantidade': 1}], self.cliente)
        self.assertEqual(pedido.status, Pedido.Status.AGUARDANDO_PAGAMENTO)
        self.assertGreater(pedido.total, 0)

    def test_canal_pedido_obrigatorio(self):
        with self.assertRaises(Exception):
            criar_pedido(self.cliente, self.unidade.id, '', [{'produtoId': self.produto.id, 'quantidade': 1}], self.cliente)
