from django.urls import path
from orders.infrastructure.views import CustomerListView, CustomerDetailView
from orders.infrastructure.views_product import ProductListView, ProductStockUpdateView

urlpatterns = [
    path('v1/customers', CustomerListView.as_view(), name='customers-list'),
    path('v1/customers/<int:id>', CustomerDetailView.as_view(), name='customers-detail'),
    path('v1/products', ProductListView.as_view(), name='products-list'),
    path('v1/products/<str:sku>/stock', ProductStockUpdateView.as_view(), name='products-stock-update'),
]