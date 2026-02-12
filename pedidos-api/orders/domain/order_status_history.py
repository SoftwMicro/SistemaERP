class OrderStatusHistory:
    def __init__(self, data_hora, status_anterior, novo_status, usuario, observacoes=None):
        self.data_hora = data_hora
        self.status_anterior = status_anterior
        self.novo_status = novo_status
        self.usuario = usuario
        self.observacoes = observacoes
