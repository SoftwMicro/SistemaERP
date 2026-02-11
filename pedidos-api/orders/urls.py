from django.urls import path
from orders.infrastructure.views import CustomerListView, CustomerDetailView

urlpatterns = [
    path('v1/customers', CustomerListView.as_view(), name='customers-list'),
    path('v1/customers/<int:id>', CustomerDetailView.as_view(), name='customers-detail'),
]