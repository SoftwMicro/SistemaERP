from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.infrastructure.singletons import product_service

class ProductListView(APIView):
    def get(self, request):
        produtos = product_service.listar_produtos()
        data = [p.to_dict() for p in produtos]
        return Response(data)

    def post(self, request):
        produto = product_service.criar_produto(request.data)
        return Response(produto.to_dict(), status=status.HTTP_201_CREATED)

class ProductStockUpdateView(APIView):
    def patch(self, request, sku):
        quantidade = request.data.get("stock_quantity")
        produto = product_service.atualizar_estoque(sku, quantidade)
        if produto:
            return Response(produto.to_dict())
        return Response({"error": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND)
