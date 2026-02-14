import pytest
from orders.application.order_service import OrderService
from orders.domain.order_item import OrderItem
from orders.domain.order import Order

class DummyCliente:
    def __init__(self, nome, id=1):
        self.nome = nome
        self.id = id

class DummyClienteService:
    def buscar_cliente(self, cliente_id):
        if cliente_id == 1:
            return DummyCliente('Cliente Teste', 1)
        return None

class DummyProduct:
    def __init__(self, sku, price, stock_quantity):
        self.sku = sku
        self.price = price
        self.stock_quantity = stock_quantity

class DummyProductRepository:
    def __init__(self):
        self._produtos = {'SKU1': DummyProduct('SKU1', 10.0, 5)}

    def listar(self):
        return list(self._produtos.values())

    def atualizar_estoque(self, sku, nova_quantidade):
        if sku in self._produtos:
            self._produtos[sku].stock_quantity = nova_quantidade

class DummyProductService:
    def __init__(self):
        self.repository = DummyProductRepository()

class DummyOrderRepository:
    def __init__(self):
        self._pedidos = []
        self._id_counter = 1
    def salvar(self, pedido):
        pedido.numero = self._id_counter
        self._id_counter += 1
        self._pedidos.append(pedido)
        return pedido
    def listar(self):
        return self._pedidos
    def buscar_por_id(self, pedido_id):
        for p in self._pedidos:
            if p.numero == pedido_id:
                return p
        return None

def test_criar_pedido_sucesso():
    repo = DummyOrderRepository()
    cliente_service = DummyClienteService()
    product_service = DummyProductService()
    service = OrderService(repo, cliente_service, product_service)
    dados = {
        'cliente_id': 1,
        'itens': [{'produto': 'SKU1', 'quantidade': 2}],
        'observacoes': 'Teste'
    }
    pedido = service.criar_pedido(dados)
    assert pedido.numero == 1
    assert pedido.valor_total == 20.0
    assert product_service.repository._produtos['SKU1'].stock_quantity == 3

def test_criar_pedido_estoque_insuficiente():
    repo = DummyOrderRepository()
    cliente_service = DummyClienteService()
    product_service = DummyProductService()
    service = OrderService(repo, cliente_service, product_service)
    dados = {
        'cliente_id': 1,
        'itens': [{'produto': 'SKU1', 'quantidade': 10}],
        'observacoes': 'Teste'
    }
    with pytest.raises(ValueError):
        service.criar_pedido(dados)

def test_cancelar_pedido_devolve_estoque():
    repo = DummyOrderRepository()
    cliente_service = DummyClienteService()
    product_service = DummyProductService()
    service = OrderService(repo, cliente_service, product_service)
    dados = {
        'cliente_id': 1,
        'itens': [{'produto': 'SKU1', 'quantidade': 2}],
        'observacoes': 'Teste'
    }
    pedido = service.criar_pedido(dados)
    assert product_service.repository._produtos['SKU1'].stock_quantity == 3
    service.cancelar_pedido(pedido.numero, usuario='admin')
    assert product_service.repository._produtos['SKU1'].stock_quantity == 5

def test_transicao_invalida_status():
    repo = DummyOrderRepository()
    cliente_service = DummyClienteService()
    product_service = DummyProductService()
    service = OrderService(repo, cliente_service, product_service)
    dados = {
        'cliente_id': 1,
        'itens': [{'produto': 'SKU1', 'quantidade': 1}],
        'observacoes': 'Teste'
    }
    pedido = service.criar_pedido(dados)
    with pytest.raises(ValueError):
        service.alterar_status(pedido.numero, 'ENTREGUE', usuario='admin')
