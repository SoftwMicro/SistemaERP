import pytest
from orders.domain.order import Order
from orders.domain.order_item import OrderItem
from orders.domain.order_status_history import OrderStatusHistory
from datetime import datetime

class DummyCliente:
    def __init__(self, nome):
        self.nome = nome

def test_order_creation_and_total():
    cliente = DummyCliente('Cliente Teste')
    itens = [OrderItem('SKU1', 2, 10.0), OrderItem('SKU2', 1, 20.0)]
    order = Order(cliente, itens)
    assert order.valor_total == 40.0
    assert order.status == 'PENDENTE'
    assert order.cliente.nome == 'Cliente Teste'
    assert len(order.itens) == 2

def test_order_status_transition_and_history():
    cliente = DummyCliente('Cliente Teste')
    itens = [OrderItem('SKU1', 1, 10.0)]
    order = Order(cliente, itens)
    order.adicionar_status('CONFIRMADO', usuario='admin')
    assert order.status == 'CONFIRMADO'
    assert len(order.historico_status) == 1
    hist = order.historico_status[0]
    assert hist.status_anterior == 'PENDENTE'
    assert hist.novo_status == 'CONFIRMADO'
    assert hist.usuario == 'admin'
    assert isinstance(hist.data_hora, datetime)

def test_invalid_status_transition():
    cliente = DummyCliente('Cliente Teste')
    itens = [OrderItem('SKU1', 1, 10.0)]
    order = Order(cliente, itens)
    with pytest.raises(ValueError):
        order.adicionar_status('INVALIDO', usuario='admin')
