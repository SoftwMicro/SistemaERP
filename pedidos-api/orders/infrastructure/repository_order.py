from orders.domain.order import Order

class OrderRepositoryMemoria:
    def __init__(self):
        self._pedidos = []
        self._id_counter = 1

    def salvar(self, pedido):
        if not pedido.numero:
            pedido.numero = self._id_counter
            self._id_counter += 1
        self._pedidos.append(pedido)
        return pedido

    def listar(self):
        return self._pedidos

    def buscar_por_id(self, pedido_id):
        for pedido in self._pedidos:
            if pedido.numero == pedido_id:
                return pedido
        return None
