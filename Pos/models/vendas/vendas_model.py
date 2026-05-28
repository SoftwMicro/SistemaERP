from models.pedido_model import PedidoModel
from models.status_history_model import StatusHistoryModel
from models.produto_model import ProdutoModel
from utils.messages import Messages

class VendasModel:
    @staticmethod
    def listar_pedidos():
        # Retorna todos os pedidos com nome do cliente
        pedidos = PedidoModel.listar_todos()
        for p in pedidos:
            p['cliente'] = p.get('cliente_nome', '')
        return pedidos

    @staticmethod
    def cancelar_pedido(pedido_id, usuario):
        try:
            pedido = PedidoModel.buscar_por_id(pedido_id)
            if not pedido:
                return False, Messages.ERROR_GENERIC
            PedidoModel.atualizar_status(pedido_id, "CANCELADO")
            StatusHistoryModel.inserir_status(
                pedido_id=pedido_id,
                status_anterior=pedido['status'],
                novo_status="CANCELADO",
                usuario=usuario
            )
            return True, Messages.SUCCESS_CANCEL
        except Exception as e:
            return False, f"{Messages.ERROR_TRANSACTION} Detalhe: {e}"

    @staticmethod
    def deletar_pedido(pedido_id):
        try:
            pedido = PedidoModel.buscar_por_id(pedido_id)
            if not pedido:
                return False, Messages.ERROR_GENERIC
            itens = PedidoModel.buscar_itens_pedido(pedido_id)
            for item in itens:
                ProdutoModel.atualizar_estoque(item['produto_id'], -item['quantidade'])
            PedidoModel.deletar_pedido(pedido_id)
            return True, Messages.SUCCESS_DELETE
        except Exception as e:
            return False, f"{Messages.ERROR_TRANSACTION} Detalhe: {e}"
