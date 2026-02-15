
from orders.domain.order import Order
from orders.domain.order_item import OrderItem
from orders.domain.order_status_history import OrderStatusHistory
from orders.infrastructure.redis_services import RedisLock, RedisIdempotency

class OrderService:
    def __init__(self, repository, cliente_service, product_service):
        self.repository = repository
        self.cliente_service = cliente_service
        self.product_service = product_service

    def criar_pedido(self, dados):
        redis_lock = RedisLock()
        redis_idemp = RedisIdempotency()
        idempotency_key = dados.get('idempotency_key')
        if idempotency_key:
            pedido_id = redis_idemp.get_pedido_id(idempotency_key)
            if pedido_id:
                pedido = self.repository.buscar_por_id(pedido_id)
                if pedido:
                    return pedido
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
        locked_skus = []
        produtos_info = {}
        try:
            # Primeiro: Lock e checagem de estoque para todos os itens
            for item in dados['itens']:
                produto = self.product_service.repository.listar()
                produto = next((p for p in produto if p.sku == item['produto']), None)
                if not produto:
                    raise ValueError(f"Produto {item['produto']} não encontrado")
                if hasattr(produto, 'is_active') and not produto.is_active:
                    raise ValueError(f"Produto {item['produto']} inativo")
                # Lock por SKU
                if not redis_lock.acquire_lock(produto.sku, idempotency_key or 'pedido_temp'):
                    raise ValueError(f"Concorrência: Produto {produto.sku} está sendo reservado")
                locked_skus.append(produto.sku)
                # Checagem de estoque
                produto_atual = self.product_service.repository.listar()
                produto_atual = next((p for p in produto_atual if p.sku == item['produto']), None)
                if produto_atual.stock_quantity < item['quantidade']:
                    raise ValueError(f"Estoque insuficiente para o produto {produto.sku}")
                # Guarda info para segunda etapa
                produtos_info[produto.sku] = {
                    'produto': produto,
                    'quantidade': item['quantidade'],
                    'preco': produto.price,
                    'stock_quantity': produto_atual.stock_quantity
                }
            # Segundo: Só agora faz a reserva de estoque e monta os itens
            for sku, info in produtos_info.items():
                self.product_service.repository.atualizar_estoque(sku, info['stock_quantity'] - info['quantidade'])
                itens.append(OrderItem(produto=sku, quantidade=info['quantidade'], preco_unitario=info['preco']))
        except Exception as e:
            # Libera locks em caso de erro
            for sku in locked_skus:
                redis_lock.release_lock(sku)
            raise
        # Cria pedido
        pedido = Order(cliente=cliente, itens=itens, observacoes=dados.get('observacoes'))
        pedido.idempotency_key = idempotency_key
        self.repository.salvar(pedido)
        # Salva idempotency no Redis
        if idempotency_key:
            redis_idemp.save_key(idempotency_key, pedido.numero)
        # Libera locks
        for sku in locked_skus:
            redis_lock.release_lock(sku)
        return pedido

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
