from dataclasses import dataclass
from datetime import datetime


@dataclass
class Pagamento:
    """Modelo de dados para Pagamento."""

    id: int | None
    pedido_id: int
    forma_pagamento: str  # Dinheiro, Cartão, Pix
    valor_pago: float
    data_pagamento: datetime
    status_pagamento: str  # Pendente, Confirmado, Recusado
    observacoes: str | None = None
