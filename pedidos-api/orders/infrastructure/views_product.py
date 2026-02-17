from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.infrastructure.singletons import product_service

class ProductListView(APIView):
    def get(self, request):
        """
        Lista todos os produtos.
        Exemplo de resposta:
        [
            {
                "sku": "PROD001",
                "nome": "Produto Exemplo",
                "preco": 99.99,
                "estoque": 10
            }
        ]
        """
        produtos = product_service.listar_produtos()
        data = [p.to_dict() for p in produtos]
        return Response(data)

    def post(self, request):
        """
        Cria um novo produto.
        Exemplo de entrada:
        {
            "sku": "PROD002",
            "nome": "Produto Novo",
            "preco": 49.90,
            "estoque": 20
        }
        """
        produto = product_service.criar_produto(request.data)
        return Response(produto.to_dict(), status=status.HTTP_201_CREATED)

class ProductStockUpdateView(APIView):
    def patch(self, request, sku):
        """
        Atualiza o estoque de um produto.
        Exemplo de entrada:
        {
            "stock_quantity": 15
        }
        """
        quantidade = request.data.get("stock_quantity")
        produto = product_service.atualizar_estoque(sku, quantidade)
        if produto:
            return Response(produto.to_dict())
        return Response({"error": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND)
