from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

from apps.usuarios.views import UsuarioViewSet, LoginView
from apps.unidades.views import UnidadeViewSet
from apps.produtos.views import ProdutoViewSet, CardapioItemViewSet
from apps.estoque.views import EstoqueViewSet
from apps.pedidos.views import PedidoViewSet
from apps.pagamentos.views import PagamentoMockView
from apps.fidelidade.views import FidelidadeViewSet
from apps.auditoria.views import LogAuditoriaViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'unidades', UnidadeViewSet, basename='unidades')
router.register(r'produtos', ProdutoViewSet, basename='produtos')
router.register(r'cardapio', CardapioItemViewSet, basename='cardapio')
router.register(r'estoques', EstoqueViewSet, basename='estoques')
router.register(r'pedidos', PedidoViewSet, basename='pedidos')
router.register(r'fidelidade', FidelidadeViewSet, basename='fidelidade')
router.register(r'auditoria/logs', LogAuditoriaViewSet, basename='auditoria-logs')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/pagamentos/mock/', PagamentoMockView.as_view(), name='pagamento-mock'),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
