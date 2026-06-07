from dataclasses import dataclass


@dataclass
class Usuario:
    id: int | None
    nome: str
    login: str
    senha_hash: str
    perfil: str
    ativo: bool = True
