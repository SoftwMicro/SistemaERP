from django.urls import path
from .views import OrderMockView

urlpatterns = [
    path('', OrderMockView.as_view(), name='orders-mock'),
]