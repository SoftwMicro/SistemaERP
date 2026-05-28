from models.vendas.vendas_model import VendasModel
from utils.messages import Messages

class VendasController:
    def listar_pedidos(self):
        return VendasModel.listar_pedidos()

    def cancelar_pedido(self, pedido_id, usuario):
        return VendasModel.cancelar_pedido(pedido_id, usuario)

    def deletar_pedido(self, pedido_id):
        return VendasModel.deletar_pedido(pedido_id)
