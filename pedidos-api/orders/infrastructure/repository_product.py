from orders.domain.product import Product
from orders.application.product_service import ProductRepository

class ProductRepositoryMemoria(ProductRepository):
    _produtos = {}

    def criar(self, dados):
        produto = Product(
            sku=dados.get("sku"),
            name=dados.get("name"),
            description=dados.get("description"),
            price=dados.get("price"),
            stock_quantity=dados.get("stock_quantity", 0),
            is_active=dados.get("is_active", True)
        )
        self._produtos[produto.sku] = produto
        return produto

    def listar(self):
        return list(self._produtos.values())

    def atualizar_estoque(self, sku, quantidade):
        produto = self._produtos.get(sku)
        if produto:
            produto.stock_quantity = quantidade
            return produto
        return None
