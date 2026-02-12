from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.application.client_service import ClienteService
from orders.infrastructure.repository import ClienteRepositoryMemoria

cliente_service = ClienteService(repository=ClienteRepositoryMemoria())



class ApiRootView(APIView):
    """
    GET - /api/v1/ -> Lista todos os endpoints disponíveis
    """
    def get(self, request):
        return Response({
            "customers": {
                "list": "/api/v1/customers",
                "create": "/api/v1/customers",
                "detail": "/api/v1/customers/<id>"
            },
            "products": {
                "list": "/api/v1/products",
                "create": "/api/v1/products",
                "update_stock": "/api/v1/products/<sku>/stock"
            },
            "orders": {
                "list": "/api/v1/orders",
                "create": "/api/v1/orders",
                "detail": "/api/v1/orders/<id>",
                "update_status": "/api/v1/orders/<id>/status",
                "cancel": "/api/v1/orders/<id>"
            }
        })


class CustomerListView(APIView):
    def get(self, request):
        clientes = cliente_service.listar_clientes()
        data = [vars(c) for c in clientes]
        return Response(data)

    def post(self, request):
        cliente = cliente_service.criar_cliente(request.data)
        return Response(vars(cliente), status=status.HTTP_201_CREATED)


class CustomerDetailView(APIView):
    def get(self, request, id):
        cliente = cliente_service.buscar_cliente(id)
        if cliente:
            return Response(vars(cliente))
        return Response({"error": "Cliente não encontrado"}, status=status.HTTP_404_NOT_FOUND)