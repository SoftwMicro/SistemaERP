from orders.domain.order import Order
from orders.domain.order_item import OrderItem
from orders.domain.order_status_history import OrderStatusHistory

class OrderService:
    def __init__(self, repository, cliente_service):
        self.repository = repository
        self.cliente_service = cliente_service

    def criar_pedido(self, dados):
        cliente = self.cliente_service.buscar_cliente(dados['cliente_id'])
        if not cliente:
            raise ValueError('Cliente não encontrado')
        itens = [OrderItem(**item) for item in dados['itens']]
        pedido = Order(cliente=cliente, itens=itens, observacoes=dados.get('observacoes'))
        self.repository.salvar(pedido)
        return pedido

    def listar_pedidos(self):
        return self.repository.listar()

    def obter_pedido(self, pedido_id):
        return self.repository.buscar_por_id(pedido_id)

    def alterar_status(self, pedido_id, novo_status, usuario, observacoes=None):
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            raise ValueError('Pedido não encontrado')
        pedido.adicionar_status(novo_status, usuario, observacoes)
        return pedido

    def cancelar_pedido(self, pedido_id, usuario, observacoes=None):
        return self.alterar_status(pedido_id, 'CANCELADO', usuario, observacoes)
