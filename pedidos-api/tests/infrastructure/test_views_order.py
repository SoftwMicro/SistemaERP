import pytest
pytest_plugins = ['pytest_order']
from orders.domain.client import Cliente
from orders.infrastructure.singletons import cliente_service

# Fixture para garantir cliente no repositório em memória
@pytest.fixture
def cliente_memoria():
    cliente_data = {
        'nome': 'Cliente Teste',
        'cpf_cnpj': '12345678900',
        'email': 'cliente@teste.com',
        'telefone': '11999999999',
        'endereco': 'Rua Teste, 123'
    }
    # ClienteRepository usa ORM, não é necessário manipular _clientes
    return cliente_data
import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db(transaction=True)
@pytest.mark.order(1)
def test_criar_cliente_api():
    import random, string
    client = APIClient()
    rand = ''.join(random.choices(string.digits, k=5))
    resp = client.post('/api/v1/customers', {
        'nome': f'Cliente Teste {rand}',
        'cpf_cnpj': f'{random.randint(10000000000,99999999999)}',
        'email': f'cliente{rand}@teste.com',
        'telefone': f'11999{rand}',
        'endereco': f'Rua Teste, {rand}'
    }, format='json')
    assert resp.status_code == 201
    assert 'nome' in resp.data
    assert resp.data['nome'].startswith('Cliente Teste')

@pytest.mark.django_db
@pytest.mark.order(2)
def test_criar_produto_api():
    import random, string
    client = APIClient()
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    nome = random.choice(['Material X', 'Insumo Y', 'Peça Z', 'Componente W'])
    resp = client.post('/api/v1/products', {
        'sku': f'SKU{rand}',
        'name': f'{nome} {rand}',
        'description': f'Descrição do {nome}',
        'price': round(random.uniform(5, 100), 2),
        'stock_quantity': random.randint(1, 20)
    }, format='json')
    assert resp.status_code == 201
    assert resp.data['sku'].startswith('SKU')
    assert resp.data['stock_quantity'] > 0

@pytest.mark.django_db
@pytest.mark.order(3)
def test_criar_pedido_api():
    import random, string
    client = APIClient()
    rand = ''.join(random.choices(string.digits, k=5))
    cliente_data = {
        'nome': f'Cliente Logística {rand}',
        'cpf_cnpj': f'{random.randint(10000000000,99999999999)}',
        'email': f'logistica{rand}@teste.com',
        'telefone': f'11999{rand}',
        'endereco': f'Rua Logística, {rand}'
    }
    cliente = client.post('/api/v1/customers', cliente_data, format='json').data
    nome_produto = random.choice(['Material X', 'Insumo Y', 'Peça Z', 'Componente W'])
    sku = f'SKU{rand}'
    produto = client.post('/api/v1/products', {
        'sku': sku,
        'name': f'{nome_produto} {rand}',
        'description': f'Descrição do {nome_produto}',
        'price': round(random.uniform(5, 100), 2),
        'stock_quantity': random.randint(5, 20)
    }, format='json').data
    # Cliente já está persistido via API, não é necessário manipular repositório em memória

    quantidade = random.randint(1, 4)
    resp = client.post('/api/v1/orders', {
        'cliente_id': cliente['id'],
        'itens': [{'produto': sku, 'quantidade': quantidade}],
        'observacoes': f'Pedido de {nome_produto} para logística'
    }, format='json')
    print('Resposta da API ao criar pedido:', resp.data)
    assert resp.status_code == 201
    assert resp.data['status'] == 'PENDENTE'
    assert float(resp.data['valor_total']) == pytest.approx(produto['price'] * quantidade, 0.01)

@pytest.mark.django_db
@pytest.mark.order(4)
def test_criar_pedido_estoque_insuficiente_api(cliente_memoria):
    client = APIClient()
    # Cliente já está no repositório em memória
    cliente = client.post('/api/v1/customers', {
        'nome': 'Cliente Teste',
        'cpf_cnpj': '12345678900',
        'email': 'cliente@teste.com',
        'telefone': '11999999999',
        'endereco': 'Rua Teste, 123'
    }, format='json').data
    client.post('/api/v1/products', {
        'sku': 'SKU1',
        'name': 'Produto Teste',
        'description': 'Desc',
        'price': 10.0,
        'stock_quantity': 1
    }, format='json')
    resp = client.post('/api/v1/orders', {
        'cliente_id': cliente['id'],
        'itens': [{'produto': 'SKU1', 'quantidade': 2}],
        'observacoes': 'Teste'
    }, format='json')
    assert resp.status_code == 400
    assert 'estoque' in resp.data['error'].lower() or 'insuficiente' in resp.data['error'].lower()

@pytest.mark.django_db
@pytest.mark.order(5)
def test_cancelar_pedido_api():
    client = APIClient()
    cliente = client.post('/api/v1/customers', {
        'nome': 'Cliente Teste',
        'cpf_cnpj': '12345678900',
        'email': 'cliente@teste.com',
        'telefone': '11999999999',
        'endereco': 'Rua Teste, 123'
    }, format='json').data
    client.post('/api/v1/products', {
        'sku': 'SKU1',
        'name': 'Produto Teste',
        'description': 'Desc',
        'price': 10.0,
        'stock_quantity': 5
    }, format='json')
    pedido = client.post('/api/v1/orders', {
        'cliente_id': cliente['id'],
        'itens': [{'produto': 'SKU1', 'quantidade': 2}],
        'observacoes': 'Teste'
    }, format='json').data
    resp = client.delete(f"/api/v1/orders/{pedido['numero']}")
    assert resp.status_code == 200
    assert resp.data['status'] == 'CANCELADO'

@pytest.mark.django_db
@pytest.mark.order(6)
def test_transicao_invalida_status_api():
    client = APIClient()
    cliente = client.post('/api/v1/customers', {
        'nome': 'Cliente Teste',
        'cpf_cnpj': '12345678900',
        'email': 'cliente@teste.com',
        'telefone': '11999999999',
        'endereco': 'Rua Teste, 123'
    }, format='json').data
    client.post('/api/v1/products', {
        'sku': 'SKU1',
        'name': 'Produto Teste',
        'description': 'Desc',
        'price': 10.0,
        'stock_quantity': 5
    }, format='json')
    pedido = client.post('/api/v1/orders', {
        'cliente_id': cliente['id'],
        'itens': [{'produto': 'SKU1', 'quantidade': 2}],
        'observacoes': 'Teste'
    }, format='json').data
    resp = client.patch(f"/api/v1/orders/{pedido['numero']}/status", {
        'status': 'ENTREGUE',
        'usuario': 'admin'
    }, format='json')
    assert resp.status_code == 400
    assert 'transição' in resp.data['error'].lower() or 'inválida' in resp.data['error'].lower()
