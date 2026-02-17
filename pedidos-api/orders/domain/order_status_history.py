class OrderStatusHistory:
    def __init__(self, data_hora, status_anterior, novo_status, usuario, idempotency_key, observacoes=None):
        self.data_hora = data_hora
        self.status_anterior = status_anterior
        self.novo_status = novo_status
        self.usuario = usuario
        self.idempotency_key = idempotency_key
        self.observacoes = observacoes
