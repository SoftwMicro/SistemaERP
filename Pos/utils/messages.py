class Messages:
    SUCCESS_SALE = "Venda realizada com sucesso."
    ERROR_GENERIC = "Ocorreu um erro. Tente novamente."
    ERROR_CLIENT_NOT_ACTIVE = "Cliente inativo."
    ERROR_PRODUCT_NOT_ACTIVE = "Produto inativo."
    ERROR_STOCK = "Estoque insuficiente."
    ERROR_NO_CLIENT = "Selecione um cliente para prosseguir."
    ERROR_NO_PRODUCTS = "Adicione ao menos um produto ao carrinho."
    SUCCESS_CANCEL = "Pedido cancelado com sucesso."
    SUCCESS_DELETE = "Pedido deletado com sucesso."
    ERROR_TRANSACTION = "Erro na transação. Nenhuma alteração foi realizada."
    @staticmethod
    def feedback(message, success=True):
        return message