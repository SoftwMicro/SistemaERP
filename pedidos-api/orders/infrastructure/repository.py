from orders.domain.client import Cliente

class ClienteRepositoryMemoria:
    def __init__(self):
        self._clientes = []
        self._id_counter = 1

    def criar(self, dados):
        cliente = Cliente(**dados)
        cliente.id = self._id_counter
        self._id_counter += 1
        self._clientes.append(cliente)
        return cliente

    def listar(self):
        return self._clientes

    def buscar_por_id(self, cliente_id):
        for cliente in self._clientes:
            if cliente.id == cliente_id:
                return cliente
        return None