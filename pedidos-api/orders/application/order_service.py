
from orders.domain.order import Order
from orders.domain.order_item import OrderItem
from orders.domain.order_status_history import OrderStatusHistory

class OrderService:
    def __init__(self, repository, cliente_service, product_service):
        self.repository = repository
        self.cliente_service = cliente_service
        self.product_service = product_service

    def criar_pedido(self, dados):
        idempotency_key = dados.get('idempotency_key')
        if idempotency_key:
            pedido_existente = getattr(self.repository, 'buscar_por_idempotency_key', lambda k: None)(idempotency_key)
            if pedido_existente:
                return pedido_existente
        cliente = self.cliente_service.buscar_cliente(dados['cliente_id'])
        if not cliente:
            raise ValueError('Cliente não encontrado')
        if hasattr(cliente, 'ativo') and not cliente.ativo:
            raise ValueError('Cliente inativo')
        itens = []
        # Validar quantidade de itens
        if not dados['itens'] or any(item.get('quantidade', 0) <= 0 for item in dados['itens']):
            raise ValueError('A quantidade de itens deve ser maior que zero')
        # Verificar estoque de todos os produtos (tudo ou nada)
        for item in dados['itens']:
            produto = self.product_service.repository.listar()
            produto = next((p for p in produto if p.sku == item['produto']), None)
            if not produto:
                raise ValueError(f"Produto {item['produto']} não encontrado")
            if hasattr(produto, 'is_active') and not produto.is_active:
                raise ValueError(f"Produto {item['produto']} inativo")
            if produto.stock_quantity < item['quantidade']:
                raise ValueError(f"Estoque insuficiente para o produto {produto.sku}")
            itens.append(OrderItem(produto=produto.sku, quantidade=item['quantidade'], preco_unitario=produto.price))

        # Reservar estoque (atômico)
        for item in dados['itens']:
            self.product_service.repository.atualizar_estoque(item['produto'],
                self.product_service.repository.listar()
                and next((p.stock_quantity - item['quantidade'] for p in self.product_service.repository.listar() if p.sku == item['produto']), 0)
            )

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
            produto = self.product_service.repository.listar()
            produto = next((p for p in produto if p.sku == item.produto), None)
            if produto:
                self.product_service.repository.atualizar_estoque(produto.sku, produto.stock_quantity + item.quantidade)
        return self.alterar_status(pedido_id, 'CANCELADO', usuario, observacoes)
