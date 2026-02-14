from orders.models import Order as OrderModel, OrderItem as OrderItemModel, Produto as ProdutoModel
from orders.domain.order import Order
from orders.domain.order_item import OrderItem

class OrderRepository:
    def salvar(self, pedido: Order):
        # Cria o pedido no banco de dados
        order_model = OrderModel.objects.create(
            cliente=pedido.cliente,
            valor_total=pedido.valor_total,
            observacoes=pedido.observacoes or ""
        )
        for item in pedido.itens:
            produto_model = ProdutoModel.objects.get(sku=item.produto)
            OrderItemModel.objects.create(
                pedido=order_model,
                produto=produto_model,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario,
                subtotal=item.subtotal
            )
        pedido.numero = order_model.id
        return pedido

    def listar(self):
        pedidos = []
        for order_model in OrderModel.objects.all():
            itens = [OrderItem(
                produto=item.produto.sku,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario
            ) for item in order_model.itens.all()]
            pedido = Order(
                cliente=order_model.cliente,
                itens=itens,
                observacoes=order_model.observacoes
            )
            pedido.numero = order_model.id
            pedido.data_criacao = order_model.data_criacao
            pedido.status = order_model.status
            pedido.valor_total = order_model.valor_total
            pedidos.append(pedido)
        return pedidos

    def buscar_por_id(self, pedido_id):
        try:
            order_model = OrderModel.objects.get(id=pedido_id)
            itens = [OrderItem(
                produto=item.produto.sku,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario
            ) for item in order_model.itens.all()]
            pedido = Order(
                cliente=order_model.cliente,
                itens=itens,
                observacoes=order_model.observacoes
            )
            pedido.numero = order_model.id
            pedido.data_criacao = order_model.data_criacao
            pedido.status = order_model.status
            pedido.valor_total = order_model.valor_total
            return pedido
        except OrderModel.DoesNotExist:
            return None
