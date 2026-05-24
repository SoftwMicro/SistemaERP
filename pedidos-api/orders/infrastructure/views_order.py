
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from orders.infrastructure.singletons import order_service
from orders.infrastructure.serializers.order import OrderSerializer, OrderItemSerializer, OrderStatusHistorySerializer



class OrderListCreateView(APIView):
    @swagger_auto_schema(
        responses={200: OrderSerializer(many=True)},
        operation_description="Lista todos os pedidos."
    )
    def get(self, request):
        """
        Lista todos os pedidos.
        Exemplo de resposta:
        [
            {
                "numero": 1,
                "data_criacao": "2024-01-01T10:00:00",
                "cliente": "João Silva",
                "status": "PENDENTE",
                "valor_total": 199.99,
                "observacoes": "Pedido urgente",
                "itens": [
                    {
                        "produto": "Produto Exemplo",
                        "quantidade": 2,
                        "preco_unitario": 99.99,
                        "subtotal": 199.98
                    }
                ],
                "historico_status": []
            }
        ]
        """
        pedidos = order_service.listar_pedidos()
        data = [OrderSerializer(p).data for p in pedidos]
        return Response(data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'cliente': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID do cliente'),
                'itens': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'produto': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID do produto'),
                            'quantidade': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantidade')
                        },
                        required=['produto', 'quantidade']
                    )
                ),
                'observacoes': openapi.Schema(type=openapi.TYPE_STRING, description='Observações', default='')
            },
            required=['cliente', 'itens']
        ),
        responses={201: OrderSerializer},
        operation_description="Cria um novo pedido."
    )
    def post(self, request):
        """
        Cria um novo pedido.
        Exemplo de entrada:
        {
            "cliente": 1,
            "itens": [
                {"produto": 1, "quantidade": 2}
            ],
            "observacoes": "Pedido urgente"
        }
        """
        try:
            pedido = order_service.criar_pedido(request.data)
            return Response(OrderSerializer(pedido).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    @swagger_auto_schema(
        responses={200: OrderSerializer, 404: 'Pedido não encontrado'},
        operation_description="Obtém detalhes de um pedido."
    )
    def get(self, request, id):
        pedido = order_service.obter_pedido(id)
        if pedido:
            return Response(OrderSerializer(pedido).data)
        return Response({'error': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={200: OrderSerializer, 400: 'Erro ao cancelar pedido'},
        operation_description="Cancela um pedido."
    )
    def delete(self, request, id):
        try:
            pedido = order_service.cancelar_pedido(id, usuario='sistema')
            return Response(OrderSerializer(pedido).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderStatusUpdateView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Novo status'),
                'usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Usuário', default='sistema'),
                'observacoes': openapi.Schema(type=openapi.TYPE_STRING, description='Observações', default='')
            },
            required=['status']
        ),
        responses={200: OrderSerializer, 400: 'Erro ao alterar status'},
        operation_description="Altera o status de um pedido."
    )
    def patch(self, request, id):
        novo_status = request.data.get('status')
        usuario = request.data.get('usuario', 'sistema')
        observacoes = request.data.get('observacoes')
        try:
            pedido = order_service.alterar_status(id, novo_status, usuario, observacoes)
            return Response(OrderSerializer(pedido).data())
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
