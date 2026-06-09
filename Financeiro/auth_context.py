from typing import Optional

from .model.user import Usuario

_current_user: Optional[Usuario] = None


def set_current_user(usuario: Usuario) -> None:
    global _current_user
    _current_user = usuario


def get_current_user() -> Optional[Usuario]:
    return _current_user
