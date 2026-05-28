from datetime import datetime
from models.pedido_model import PedidoModel
from models.item_model import ItemModel
from models.status_history_model import StatusHistoryModel
from models.produto_model import ProdutoModel
from utils.messages import Messages
from database.db_connection import DatabaseConnection

class PedidoController:
    def __init__(self):
        self.carrinho = []  # Lista de dicionários: {produto_id, nome, quantidade, preco_unitario, subtotal}
        self.cliente = None

    def selecionar_cliente(self, cliente):
        self.cliente = cliente

    def adicionar_produto(self, produto, quantidade):
        if not produto['ativo']:
            return Messages.ERROR_PRODUCT_NOT_ACTIVE
        if produto['quantidade_estoque'] < quantidade:
            return Messages.ERROR_STOCK
        for item in self.carrinho:
            if item['produto_id'] == produto['id']:
                item['quantidade'] += quantidade
                item['subtotal'] = item['quantidade'] * item['preco_unitario']
                return Messages.feedback("Produto atualizado no carrinho.")
        self.carrinho.append({
            'produto_id': produto['id'],
            'nome': produto['nome'],
            'quantidade': quantidade,
            'preco_unitario': produto['preco'],
            'subtotal': quantidade * produto['preco']
        })
        return Messages.feedback("Produto adicionado ao carrinho.")

    def remover_produto(self, produto_id):
        self.carrinho = [item for item in self.carrinho if item['produto_id'] != produto_id]
        return Messages.feedback("Produto removido do carrinho.")

    def limpar_carrinho(self):
        self.carrinho = []

    def valor_total(self):
        return sum(item['subtotal'] for item in self.carrinho)

    def pode_finalizar(self):
        if not self.cliente:
            return False, Messages.ERROR_NO_CLIENT
        if not self.carrinho:
            return False, Messages.ERROR_NO_PRODUCTS
        return True, None

    def finalizar_pedido(self, observacoes, usuario):
        pode, msg = self.pode_finalizar()
        if not pode:
            return False, msg
        db = None
        try:
            db = DatabaseConnection()
            conn = db.get_connection()
            conn.start_transaction()
            pedido_id = PedidoModel.criar_pedido(
                data_criacao=datetime.now(),  # Use NOW() no SQL ou passe datetime.now()
                status="ABERTO",
                valor_total=self.valor_total(),
                observacoes=observacoes,
                cliente_id=self.cliente['id']
            )
            ItemModel.inserir_itens(pedido_id, self.carrinho)
            for item in self.carrinho:
                ProdutoModel.atualizar_estoque(item['produto_id'], item['quantidade'])
            StatusHistoryModel.inserir_status(
                pedido_id=pedido_id,
                status_anterior="",
                novo_status="ABERTO",
                usuario=usuario,
                observacoes=observacoes
            )
            conn.commit()
            self.limpar_carrinho()
            return True, Messages.SUCCESS_SALE
        except Exception as e:
            if db and db.connection:
                db.connection.rollback()
            return False, f"{Messages.ERROR_TRANSACTION} Detalhe: {e}"
        finally:
            if db:
                db.close()

    def cancelar_pedido(self, pedido_id, usuario):
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

    def deletar_pedido(self, pedido_id):
        try:
            pedido = PedidoModel.buscar_por_id(pedido_id)
            if not pedido:
                return False, Messages.ERROR_GENERIC
            itens = PedidoModel.buscar_itens_pedido(pedido_id)
            for item in itens:
                ProdutoModel.atualizar_estoque(item['produto_id'], -item['quantidade'])  # Repor estoque
            PedidoModel.deletar_pedido(pedido_id)
            return True, Messages.SUCCESS_DELETE
        except Exception as e:
            return False, f"{Messages.ERROR_TRANSACTION} Detalhe: {e}"
