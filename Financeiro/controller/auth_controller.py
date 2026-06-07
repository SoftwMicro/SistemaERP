from ..model.user import Usuario
from ..repository.user_repository import UserRepository
from ..utils.password import hash_password, verify_password


class AuthController:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def login(self, login: str, senha: str) -> Usuario:
        if not login or not senha:
            raise ValueError("Login e senha são obrigatórios")

        usuario = self.repository.get_by_login(login)
        if usuario is None:
            raise ValueError("Usuário ou senha inválidos")

        if not usuario.ativo:
            raise PermissionError("Usuário inativo")

        if not verify_password(senha, usuario.senha_hash):
            raise ValueError("Usuário ou senha inválidos")

        return usuario

    def register_user(
        self,
        nome: str,
        login: str,
        senha: str,
        perfil: str,
        ativo: bool,
    ) -> Usuario:
        if not nome or not login or not senha or not perfil:
            raise ValueError("Todos os campos obrigatórios devem ser preenchidos")

        if self.repository.get_by_login(login):
            raise ValueError("Login já está em uso")

        senha_hash = hash_password(senha)
        usuario = Usuario(
            id=None,
            nome=nome.strip(),
            login=login.strip(),
            senha_hash=senha_hash,
            perfil=perfil.strip(),
            ativo=ativo,
        )
        return self.repository.create(usuario)
