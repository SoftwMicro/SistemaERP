class OrderItem:
    def __init__(self, produto, quantidade, preco_unitario):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.subtotal = quantidade * preco_unitario
