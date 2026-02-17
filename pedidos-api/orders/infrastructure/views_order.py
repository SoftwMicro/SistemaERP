from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.infrastructure.singletons import order_service
#  Serializers simples para resposta JSON
class OrderItemSerializer:
    def __init__(self, obj):
        self.obj = obj
    def data(self):
        return {
            'produto': self.obj.produto,
            'quantidade': self.obj.quantidade,
            'preco_unitario': self.obj.preco_unitario,
            'subtotal': self.obj.subtotal
        }

class OrderStatusHistorySerializer:
    def __init__(self, obj):
        self.obj = obj
    def data(self):
        return {
            'data_hora': self.obj.data_hora.isoformat(),
            'status_anterior': self.obj.status_anterior,
            'novo_status': self.obj.novo_status,
            'usuario': self.obj.usuario,
            'observacoes': self.obj.observacoes
        }

class OrderSerializer:
    def __init__(self, obj):
        self.obj = obj
    def data(self):
        return {
            'numero': self.obj.numero,
            'data_criacao': self.obj.data_criacao.isoformat(),
            'cliente': getattr(self.obj.cliente, 'nome', str(self.obj.cliente)),
            'status': self.obj.status,
            'valor_total': self.obj.valor_total,
            'observacoes': self.obj.observacoes,
            'itens': [OrderItemSerializer(item).data() for item in self.obj.itens],
            'historico_status': [OrderStatusHistorySerializer(h).data() for h in self.obj.historico_status]
        }



class OrderListCreateView(APIView):
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
        data = [OrderSerializer(p).data() for p in pedidos]
        return Response(data)

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
            return Response(OrderSerializer(pedido).data(), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    def get(self, request, id):
        pedido = order_service.obter_pedido(id)
        if pedido:
            return Response(OrderSerializer(pedido).data())
        return Response({'error': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            pedido = order_service.cancelar_pedido(id, usuario='sistema')
            return Response(OrderSerializer(pedido).data())
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class OrderStatusUpdateView(APIView):
    def patch(self, request, id):
        novo_status = request.data.get('status')
        usuario = request.data.get('usuario', 'sistema')
        observacoes = request.data.get('observacoes')
        try:
            pedido = order_service.alterar_status(id, novo_status, usuario, observacoes)
            return Response(OrderSerializer(pedido).data())
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
