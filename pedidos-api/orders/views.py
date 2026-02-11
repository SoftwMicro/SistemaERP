from rest_framework.response import Response
from rest_framework.views import APIView

# Lista em memória simulando pedidos
ORDERS = [
    {"id": 1, "customer": "Maria", "status": "PENDING"},
    {"id": 2, "customer": "João", "status": "SHIPPED"},
]

class OrderMockView(APIView):
    def get(self, request):
        return Response(ORDERS)

    def post(self, request):
        new_order = request.data
        new_order["id"] = len(ORDERS) + 1
        ORDERS.append(new_order)
        return Response(new_order, status=201)