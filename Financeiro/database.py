from __future__ import annotations
from .config import DatabaseConfig


class Database:
    def __init__(self, config: DatabaseConfig | None = None):
        self.config = config or DatabaseConfig()

    def get_connection(self) -> "mysql.connector.connection_cext.CMySQLConnection":
        import mysql.connector

        return mysql.connector.connect(
            host=self.config.host,
            database=self.config.database,
            user=self.config.user,
            password=self.config.password,
            port=self.config.port,
        )

    def test(self) -> bool:
        from mysql.connector import Error

        try:
            with self.get_connection() as connection:
                return connection.is_connected()
        except Error:
            return False
