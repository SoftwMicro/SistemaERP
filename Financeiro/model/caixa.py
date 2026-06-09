from dataclasses import dataclass
from datetime import datetime


@dataclass
class Caixa:
    id: int | None
    usuario_id: int
    data_abertura: datetime
    data_fechamento: datetime | None = None
    saldo_inicial: float = 0.0
    saldo_final: float | None = None
    status: str = "Aberto"
