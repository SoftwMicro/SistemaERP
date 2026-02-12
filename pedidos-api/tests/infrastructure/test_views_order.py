import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_criar_cliente_api():
    client = APIClient()
    resp = client.post('/api/v1/customers', {
        'nome': 'Cliente Teste',
        'cpf_cnpj': '12345678900',
        'email': 'cliente@teste.com',
        'telefone': '11999999999',
        'endereco': 'Rua Teste, 123'
    }, format='json')
    assert resp.status_code == 201
    assert 'nome' in resp.data
    assert resp.data['nome'] == 'Cliente Teste'

@pytest.mark.django_db
def test_criar_produto_api():
    client = APIClient()
    resp = client.post('/api/v1/products', {
        'sku': 'SKU1',
        'name': 'Produto Teste',
        'description': 'Desc',
        'price': 10.0,
        'stock_quantity': 5
    }, format='json')
    assert resp.status_code == 201
    assert resp.data['sku'] == 'SKU1'
    assert resp.data['stock_quantity'] == 5

@pytest.mark.django_db
def test_criar_pedido_api():
    client = APIClient()
    # Criar cliente
    cliente = client.post('/api/v1/customers', {
        'nome': 'Cliente Teste',
        'cpf_cnpj': '12345678900',
        'email': 'cliente@teste.com',
        'telefone': '11999999999',
        'endereco': 'Rua Teste, 123'
    }, format='json').data
    # Criar produto
    produto = client.post('/api/v1/products', {
        'sku': 'SKU1',
        'name': 'Produto Teste',
        'description': 'Desc',
        'price': 10.0,
        'stock_quantity': 5
    }, format='json').data
    # Criar pedido
    resp = client.post('/api/v1/orders', {
        'cliente_id': 1,
        'itens': [{'produto': 'SKU1', 'quantidade': 2}],
        'observacoes': 'Teste'
    }, format='json')
    assert resp.status_code == 201
    assert resp.data['status'] == 'PENDENTE'
    assert resp.data['valor_total'] == 20.0

@pytest.mark.django_db
def test_criar_pedido_estoque_insuficiente_api():
    client = APIClient()
    client.post('/api/v1/customers', {
        'nome': 'Cliente Teste',
        'cpf_cnpj': '12345678900',
        'email': 'cliente@teste.com',
        'telefone': '11999999999',
        'endereco': 'Rua Teste, 123'
    }, format='json')
    client.post('/api/v1/products', {
        'sku': 'SKU1',
        'name': 'Produto Teste',
        'description': 'Desc',
        'price': 10.0,
        'stock_quantity': 1
    }, format='json')
    resp = client.post('/api/v1/orders', {
        'cliente_id': 1,
        'itens': [{'produto': 'SKU1', 'quantidade': 2}],
        'observacoes': 'Teste'
    }, format='json')
    assert resp.status_code == 400
    assert 'estoque' in resp.data['error'].lower() or 'insuficiente' in resp.data['error'].lower()

@pytest.mark.django_db
def test_cancelar_pedido_api():
    client = APIClient()
    client.post('/api/v1/customers', {
        'nome': 'Cliente Teste',
        'cpf_cnpj': '12345678900',
        'email': 'cliente@teste.com',
        'telefone': '11999999999',
        'endereco': 'Rua Teste, 123'
    }, format='json')
    client.post('/api/v1/products', {
        'sku': 'SKU1',
        'name': 'Produto Teste',
        'description': 'Desc',
        'price': 10.0,
        'stock_quantity': 5
    }, format='json')
    pedido = client.post('/api/v1/orders', {
        'cliente_id': 1,
        'itens': [{'produto': 'SKU1', 'quantidade': 2}],
        'observacoes': 'Teste'
    }, format='json').data
    resp = client.delete(f"/api/v1/orders/{pedido['numero']}")
    assert resp.status_code == 200
    assert resp.data['status'] == 'CANCELADO'

@pytest.mark.django_db
def test_transicao_invalida_status_api():
    client = APIClient()
    client.post('/api/v1/customers', {
        'nome': 'Cliente Teste',
        'cpf_cnpj': '12345678900',
        'email': 'cliente@teste.com',
        'telefone': '11999999999',
        'endereco': 'Rua Teste, 123'
    }, format='json')
    client.post('/api/v1/products', {
        'sku': 'SKU1',
        'name': 'Produto Teste',
        'description': 'Desc',
        'price': 10.0,
        'stock_quantity': 5
    }, format='json')
    pedido = client.post('/api/v1/orders', {
        'cliente_id': 1,
        'itens': [{'produto': 'SKU1', 'quantidade': 2}],
        'observacoes': 'Teste'
    }, format='json').data
    resp = client.patch(f"/api/v1/orders/{pedido['numero']}/status", {
        'status': 'ENTREGUE',
        'usuario': 'admin'
    }, format='json')
    assert resp.status_code == 400
    assert 'transição' in resp.data['error'].lower() or 'inválida' in resp.data['error'].lower()
