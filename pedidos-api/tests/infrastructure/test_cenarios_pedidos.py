import pytest
from rest_framework.test import APIClient
import threading
import time

@pytest.mark.django_db
class TestCenariosPedidos:
    def test_concorrencia_estoque(self):
        """
        Cenário 6.1: Concorrência de Estoque
        Produto X tem 10 unidades. Dois pedidos simultâneos tentam comprar 8 cada.
        Apenas um deve ser aceito.
        """
        client = APIClient()
        # Cria produto com 10 unidades
        produto = client.post('/api/v1/products', {
            'sku': 'SKU_CONC',
            'name': 'Produto Concorrente',
            'description': 'Teste concorrência',
            'price': 50.0,
            'stock_quantity': 10
        }, format='json').data
        # Cria cliente
        cliente = client.post('/api/v1/customers', {
            'nome': 'Cliente Concorrente',
            'cpf_cnpj': '11111111111',
            'email': 'concorrente@teste.com',
            'telefone': '11999999999',
            'endereco': 'Rua Concorrente, 1'
        }, format='json').data
        # Função para tentar criar pedido
        results = []
        def criar_pedido(idempotency_key):
            resp = client.post('/api/v1/orders', {
                'cliente_id': cliente['id'],
                'itens': [{'produto': 'SKU_CONC', 'quantidade': 8}],
                'observacoes': 'Concorrência',
                'idempotency_key': idempotency_key
            }, format='json')
            results.append(resp.status_code)
        # Executa em paralelo
        t1 = threading.Thread(target=criar_pedido, args=("CONC1",))
        t2 = threading.Thread(target=criar_pedido, args=("CONC2",))
        t1.start(); t2.start(); t1.join(); t2.join()
        # Apenas um pedido deve ser aceito (201), outro deve falhar (400)
        assert results.count(201) == 1
        assert results.count(400) == 1

    def test_idempotencia(self):
        """
        Cenário 6.2: Idempotência
        Envia 3 requisições POST idênticas (mesma idempotency_key).
        Apenas um pedido deve ser criado.
        """
        client = APIClient()
        produto = client.post('/api/v1/products', {
            'sku': 'SKU_IDEMP',
            'name': 'Produto Idemp',
            'description': 'Teste idempotência',
            'price': 30.0,
            'stock_quantity': 10
        }, format='json').data
        cliente = client.post('/api/v1/customers', {
            'nome': 'Cliente Idemp',
            'cpf_cnpj': '22222222222',
            'email': 'idemp@teste.com',
            'telefone': '11999999998',
            'endereco': 'Rua Idemp, 2'
        }, format='json').data
        pedido_data = {
            'cliente_id': cliente['id'],
            'itens': [{'produto': 'SKU_IDEMP', 'quantidade': 2}],
            'observacoes': 'Teste idempotência',
            'idempotency_key': 'IDEMP123'
        }
        responses = [client.post('/api/v1/orders', pedido_data, format='json') for _ in range(3)]
        codigos = [r.status_code for r in responses]
        assert codigos.count(201) + codigos.count(200) == 3
        ids = [r.data.get('numero') for r in responses]
        assert all(i == ids[0] for i in ids)  # Todos retornam o mesmo pedido

    def test_atomicidade_falha_parcial(self):
        """
        Cenário 6.3: Atomicidade em Falha Parcial
        Pedido com 3 itens, um sem estoque. Nenhum estoque deve ser reservado.
        """
        client = APIClient()
        # Cria produtos
        p1 = client.post('/api/v1/products', {
            'sku': 'SKU_ATOM1', 'name': 'Produto 1', 'description': 'P1', 'price': 10.0, 'stock_quantity': 5
        }, format='json').data
        p2 = client.post('/api/v1/products', {
            'sku': 'SKU_ATOM2', 'name': 'Produto 2', 'description': 'P2', 'price': 20.0, 'stock_quantity': 5
        }, format='json').data
        p3 = client.post('/api/v1/products', {
            'sku': 'SKU_ATOM3', 'name': 'Produto 3', 'description': 'P3', 'price': 30.0, 'stock_quantity': 0
        }, format='json').data
        cliente = client.post('/api/v1/customers', {
            'nome': 'Cliente Atom',
            'cpf_cnpj': '33333333333',
            'email': 'atom@teste.com',
            'telefone': '11999999997',
            'endereco': 'Rua Atom, 3'
        }, format='json').data
        pedido_data = {
            'cliente_id': cliente['id'],
            'itens': [
                {'produto': 'SKU_ATOM1', 'quantidade': 2},
                {'produto': 'SKU_ATOM2', 'quantidade': 2},
                {'produto': 'SKU_ATOM3', 'quantidade': 1}
            ],
            'observacoes': 'Teste atomicidade'
        }
        resp = client.post('/api/v1/orders', pedido_data, format='json')
        assert resp.status_code == 400
        # Estoque dos produtos 1 e 2 deve permanecer igual
        from orders.models import Produto
        p1_atual = Produto.objects.get(sku='SKU_ATOM1')
        p2_atual = Produto.objects.get(sku='SKU_ATOM2')
        assert p1_atual.quantidade_estoque == 5
        assert p2_atual.quantidade_estoque == 5
