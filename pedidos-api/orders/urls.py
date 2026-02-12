from django.urls import path
from orders.infrastructure.views import ApiRootView, CustomerListView, CustomerDetailView
from orders.infrastructure.views_product import ProductListView, ProductStockUpdateView
from orders.infrastructure.views_order import OrderListCreateView, OrderDetailView, OrderStatusUpdateView

urlpatterns = [
    # Página inicial da API
    path('v1/', ApiRootView.as_view(), name='api-root'),

    # Clientes
    path('v1/customers', CustomerListView.as_view(), name='customers-list'),
    path('v1/customers/<int:id>', CustomerDetailView.as_view(), name='customers-detail'),

    # Produtos
    path('v1/products', ProductListView.as_view(), name='products-list'),
    path('v1/products/<str:sku>/stock', ProductStockUpdateView.as_view(), name='products-stock-update'),

    # Pedidos
    path('v1/orders', OrderListCreateView.as_view(), name='orders-list-create'),
    path('v1/orders/<int:id>', OrderDetailView.as_view(), name='orders-detail'),
    path('v1/orders/<int:id>/status', OrderStatusUpdateView.as_view(), name='orders-status-update'),
]