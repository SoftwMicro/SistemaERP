from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.infrastructure.singletons import order_service
from orders.infrastructure.repository_client import ClienteRepository
from orders.infrastructure.repository_product import ProductRepositoryMemoria
from orders.infrastructure.repository_order import OrderRepositoryMemoria
from orders.application.client_service import ClienteService
from orders.application.product_service import ProductService
from orders.application.order_service import OrderService
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

# Instâncias globais (mock)
cliente_repository = ClienteRepository()
cliente_service = ClienteService(repository=cliente_repository)
order_repository = OrderRepositoryMemoria()
product_repository = ProductRepositoryMemoria()
product_service = ProductService(repository=product_repository)
order_service = OrderService(order_repository, cliente_service, product_service)

class OrderListCreateView(APIView):
    def get(self, request):
        pedidos = order_service.listar_pedidos()
        data = [OrderSerializer(p).data() for p in pedidos]
        return Response(data)

    def post(self, request):
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
