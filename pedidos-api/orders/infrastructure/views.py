
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from orders.infrastructure.singletons import cliente_service
from orders.models import Cliente


# Serializer para Cliente
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'cpf_cnpj', 'email', 'telefone', 'endereco', 'ativo']



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
        """
        Lista todos os clientes cadastrados.
        Exemplo de resposta:
        [
            {
                "id": 1,
                "nome": "João Silva",
                "cpf_cnpj": "123.456.789-00",
                "email": "joao@email.com",
                "telefone": "(11) 99999-9999",
                "endereco": "Rua Exemplo, 123",
                "ativo": true
            }
        ]
        """
        clientes = cliente_service.listar_clientes()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Cria um novo cliente.
        Exemplo de entrada:
        {
            "nome": "Maria Souza",
            "cpf_cnpj": "987.654.321-00",
            "email": "maria@email.com",
            "telefone": "(21) 88888-8888",
            "endereco": "Av. Teste, 456",
            "ativo": true
        }
        """
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            cliente = cliente_service.criar_cliente(serializer.validated_data)
            return Response(ClienteSerializer(cliente).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):
    def get(self, request, id):
        cliente = cliente_service.buscar_cliente(id)
        if cliente:
            return Response(ClienteSerializer(cliente).data)
        return Response({"error": "Cliente não encontrado"}, status=status.HTTP_404_NOT_FOUND)