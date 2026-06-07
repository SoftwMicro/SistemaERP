from mysql.connector import Error, IntegrityError

from ..database import Database
from ..model.user import Usuario


class UserRepository:
    def __init__(self, database: Database):
        self.database = database

    def get_by_login(self, login: str) -> Usuario | None:
        query = "SELECT id, nome, login, senha_hash, perfil, ativo FROM orders_usuario WHERE login = %s"
        with self.database.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (login,))
                row = cursor.fetchone()
                if not row:
                    return None
                return Usuario(
                    id=row["id"],
                    nome=row["nome"],
                    login=row["login"],
                    senha_hash=row["senha_hash"],
                    perfil=row["perfil"],
                    ativo=bool(row["ativo"]),
                )

    def create(self, usuario: Usuario) -> Usuario:
        query = (
            "INSERT INTO orders_usuario (nome, login, senha_hash, perfil, ativo) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        with self.database.get_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        query,
                        (
                            usuario.nome,
                            usuario.login,
                            usuario.senha_hash,
                            usuario.perfil,
                            usuario.ativo,
                        ),
                    )
                    connection.commit()
                    usuario.id = cursor.lastrowid
                    return usuario
                except IntegrityError as error:
                    connection.rollback()
                    raise ValueError("Login já existe") from error
                except Error as error:
                    connection.rollback()
                    raise RuntimeError("Erro ao criar usuário") from error

    def update(self, usuario: Usuario) -> Usuario:
        query = (
            "UPDATE orders_usuario SET nome = %s, senha_hash = %s, perfil = %s, ativo = %s "
            "WHERE login = %s"
        )
        with self.database.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        usuario.nome,
                        usuario.senha_hash,
                        usuario.perfil,
                        usuario.ativo,
                        usuario.login,
                    ),
                )
                connection.commit()
                return usuario
