from models.cliente_model import ClienteModel

class ClienteController:
    def pesquisar_clientes(self, filtro):
        return ClienteModel.pesquisar_clientes(filtro)
