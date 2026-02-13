from orders.models import Cliente

class ClienteRepository:
    def criar(self, dados):
        cliente = Cliente.objects.create(**dados)
        return cliente

    def listar(self):
        return list(Cliente.objects.all())

    def buscar_por_id(self, cliente_id):
        try:
            return Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            return None