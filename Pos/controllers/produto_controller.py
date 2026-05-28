from models.produto_model import ProdutoModel

class ProdutoController:
    def listar_produtos_disponiveis(self):
        return ProdutoModel.listar_produtos_disponiveis()
