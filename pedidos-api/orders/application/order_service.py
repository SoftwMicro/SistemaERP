
from orders.domain.order import Order
from orders.domain.order_item import OrderItem
from orders.domain.order_status_history import OrderStatusHistory

class OrderService:
    def __init__(self, repository, cliente_service, product_service):
        self.repository = repository
        self.cliente_service = cliente_service
        self.product_service = product_service

    def criar_pedido(self, dados):
        cliente = self.cliente_service.buscar_cliente(dados['cliente_id'])
        if not cliente:
            raise ValueError('Cliente não encontrado')
        itens = []
        # Verificar estoque de todos os produtos (tudo ou nada)
        for item in dados['itens']:
            produto = self.product_service.repository._produtos.get(item['produto'])
            if not produto:
                raise ValueError(f"Produto {item['produto']} não encontrado")
            if produto.stock_quantity < item['quantidade']:
                raise ValueError(f"Estoque insuficiente para o produto {produto.sku}")
            itens.append(OrderItem(produto=produto.sku, quantidade=item['quantidade'], preco_unitario=produto.price))

        # Reservar estoque (atômico)
        for item in dados['itens']:
            produto = self.product_service.repository._produtos[item['produto']]
            produto.stock_quantity -= item['quantidade']

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
        # Validação de transições
        status_atual = pedido.status
        transicoes_validas = {
            'PENDENTE': ['CONFIRMADO', 'CANCELADO'],
            'CONFIRMADO': ['SEPARADO', 'CANCELADO'],
            'SEPARADO': ['ENVIADO'],
            'ENVIADO': ['ENTREGUE'],
            'ENTREGUE': [],
            'CANCELADO': []
        }
        if novo_status not in transicoes_validas.get(status_atual, []):
            raise ValueError(f"Transição de status inválida: {status_atual} → {novo_status}")
        pedido.adicionar_status(novo_status, usuario, observacoes)
        return pedido

    def cancelar_pedido(self, pedido_id, usuario, observacoes=None):
        pedido = self.repository.buscar_por_id(pedido_id)
        if not pedido:
            raise ValueError('Pedido não encontrado')
        if pedido.status not in ['PENDENTE', 'CONFIRMADO']:
            raise ValueError('Só é possível cancelar pedidos PENDENTE ou CONFIRMADO')
        # Devolver estoque
        for item in pedido.itens:
            produto = self.product_service.repository._produtos.get(item.produto)
            if produto:
                produto.stock_quantity += item.quantidade
        return self.alterar_status(pedido_id, 'CANCELADO', usuario, observacoes)
