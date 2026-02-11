from orders.domain.product import Product

class ProductRepository:
    def criar(self, dados):
        raise NotImplementedError()
    def listar(self):
        raise NotImplementedError()
    def atualizar_estoque(self, sku, quantidade):
        raise NotImplementedError()

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def criar_produto(self, dados):
        return self.repository.criar(dados)

    def listar_produtos(self):
        return self.repository.listar()

    def atualizar_estoque(self, sku, quantidade):
        return self.repository.atualizar_estoque(sku, quantidade)
