import json
import random
import requests
import sys
from datetime import datetime

API_BASE = "http://localhost:8000/api/v1"  # Ajuste para URL de produção

def menu():
    print("\n=== Console ERP Pedidos ===")
    print("1. Incluir Cliente")
    print("2. Incluir Produto")
    print("3. Realizar Pedido Automático (dados aleatórios)")
    print("4. Consultar Pedido por Número")
    print("5. Consultar Histórico de Status de Pedido")
    print("6. Sair")
    return input("Escolha uma opção: ")

def incluir_cliente():
    dados = {
        "nome": f"Cliente {random.randint(1000,9999)}",
        "cpf_cnpj": str(random.randint(10000000000,99999999999)),
        "email": f"cliente{random.randint(1000,9999)}@teste.com",
        "telefone": f"11{random.randint(900000000,999999999)}",
        "endereco": f"Rua {random.randint(1,100)}"
    }
    resp = requests.post(f"{API_BASE}/customers", json=dados)
    print("Status:", resp.status_code)
    print("Dados:", resp.json())

def incluir_produto():
    dados = {
        "sku": f"SKU{random.randint(1000,9999)}",
        "name": f"Produto {random.randint(1000,9999)}",
        "description": "Produto gerado via console",
        "price": round(random.uniform(10,100),2),
        "stock_quantity": random.randint(1,20)
    }
    resp = requests.post(f"{API_BASE}/products", json=dados)
    print("Status:", resp.status_code)
    print("Dados:", resp.json())

def realizar_pedido_automatico():
    # Busca clientes e produtos
    clientes = requests.get(f"{API_BASE}/customers").json()
    produtos = requests.get(f"{API_BASE}/products").json()
    if not clientes or not produtos:
        print("Necessário pelo menos um cliente e um produto.")
        return
    cliente_id = random.choice(clientes)["id"]
    itens = []
    for _ in range(random.randint(1,3)):
        prod = random.choice(produtos)
        itens.append({"produto": prod["sku"], "quantidade": random.randint(1, prod["stock_quantity"])})
    pedido = {
        "cliente_id": cliente_id,
        "itens": itens,
        "observacoes": f"Pedido automático {datetime.now().isoformat()}",
        "idempotency_key": f"AUTO{random.randint(10000,99999)}"
    }
    resp = requests.post(f"{API_BASE}/orders", json=pedido)
    print("Status:", resp.status_code)
    print("Dados:", resp.json())

def consultar_pedido():
    numero = input("Número do pedido: ")
    resp = requests.get(f"{API_BASE}/orders/{numero}")
    print("Status:", resp.status_code)
    print("Dados:", resp.json())

def consultar_historico():
    numero = input("Número do pedido: ")
    resp = requests.get(f"{API_BASE}/orders/{numero}/history")
    print("Status:", resp.status_code)
    print("Dados:", resp.json())

def main():
    while True:
        op = menu()
        if op == "1":
            incluir_cliente()
        elif op == "2":
            incluir_produto()
        elif op == "3":
            realizar_pedido_automatico()
        elif op == "4":
            consultar_pedido()
        elif op == "5":
            consultar_historico()
        elif op == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
