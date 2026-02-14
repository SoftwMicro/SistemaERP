from orders.models import Produto as ProdutoModel
from orders.domain.product import Product
from orders.application.product_service import ProductRepository

class ProductRepository(ProductRepository):
    def criar(self, dados):
        produto_model = ProdutoModel.objects.create(
            sku=dados.get("sku"),
            nome=dados.get("name"),
            descricao=dados.get("description"),
            preco=dados.get("price"),
            quantidade_estoque=dados.get("stock_quantity", 0),
            ativo=dados.get("is_active", True)
        )
        produto = Product(
            sku=produto_model.sku,
            name=produto_model.nome,
            description=produto_model.descricao,
            price=produto_model.preco,
            stock_quantity=produto_model.quantidade_estoque,
            is_active=produto_model.ativo
        )
        return produto

    def listar(self):
        produtos = []
        for produto_model in ProdutoModel.objects.all():
            produto = Product(
                sku=produto_model.sku,
                name=produto_model.nome,
                description=produto_model.descricao,
                price=produto_model.preco,
                stock_quantity=produto_model.quantidade_estoque,
                is_active=produto_model.ativo
            )
            produtos.append(produto)
        return produtos

    def atualizar_estoque(self, sku, quantidade):
        try:
            produto_model = ProdutoModel.objects.get(sku=sku)
            produto_model.quantidade_estoque = quantidade
            produto_model.save()
            produto = Product(
                sku=produto_model.sku,
                name=produto_model.nome,
                description=produto_model.descricao,
                price=produto_model.preco,
                stock_quantity=produto_model.quantidade_estoque,
                is_active=produto_model.ativo
            )
            return produto
        except ProdutoModel.DoesNotExist:
            return None
