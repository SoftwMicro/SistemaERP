from datetime import datetime
from .order_item import OrderItem
from .order_status_history import OrderStatusHistory

class Order:
    STATUS_CHOICES = [
        'PENDENTE', 'CONFIRMADO', 'SEPARADO', 'ENVIADO', 'ENTREGUE', 'CANCELADO'
    ]

    def __init__(self, cliente, itens, observacoes=None):
        self.numero = None  # será gerado pelo repositório
        self.data_criacao = datetime.now()
        self.cliente = cliente
        self.status = 'PENDENTE'
        self.valor_total = sum(item.subtotal for item in itens)
        self.observacoes = observacoes
        self.itens = itens
        self.historico_status = []

    def adicionar_status(self, novo_status, usuario, observacoes=None):
        if novo_status not in self.STATUS_CHOICES:
            raise ValueError('Status inválido')
        # idempotency_key deve ser passado como atributo do pedido
        historico = OrderStatusHistory(
            data_hora=datetime.now(),
            status_anterior=self.status,
            novo_status=novo_status,
            usuario=usuario,
            idempotency_key=getattr(self, 'idempotency_key', None),
            observacoes=observacoes
        )
        self.historico_status.append(historico)
        self.status = novo_status
