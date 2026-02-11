class Cliente:
    def __init__(self, nome, cpf_cnpj, email, telefone, endereco, ativo=True):
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.ativo = ativo

    def ativar(self):
        self.ativo = True

    def inativar(self):
        self.ativo = False