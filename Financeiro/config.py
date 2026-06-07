from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    database: str = "pedidos"
    user: str = "admin"
    password: str = "010101"
    port: int = 3306
