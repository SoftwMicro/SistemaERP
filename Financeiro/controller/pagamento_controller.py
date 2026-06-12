import requests

from ..repository.pagamento_repository import PagamentoRepository


class PagamentoController:
    """Controller para gerenciar operações de pagamento."""

    BASE_URL = "http://localhost:8000/api/v1/orders"

    def __init__(self):
        """Inicializa o controller com o repository de pagamento."""
        self.pagamento_repository = PagamentoRepository()

    def obter_pedido_por_id(self, pedido_id: int) -> dict:
        """Obtém dados do pedido pela API.

        Args:
            pedido_id: ID numérico do pedido

        Returns:
            dict com os dados do pedido.

        Raises:
            ValueError: se o pedido não for encontrado
            requests.HTTPError: para outros códigos de erro HTTP
        """
        url = f"{self.BASE_URL}/{pedido_id}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 404:
            raise ValueError("Pedido não encontrado")
        resp.raise_for_status()

    def registrar_pagamento(
        self,
        pedido_id: int,
        forma_pagamento: str,
        valor_pago: float,
        observacoes: str | None = None,
    ) -> dict:
        """
        Registra um novo pagamento.

        Args:
            pedido_id: ID do pedido
            forma_pagamento: Forma de pagamento (Dinheiro, Cartão, Pix)
            valor_pago: Valor do pagamento
            observacoes: Observações opcionais

        Returns:
            Dicionário com os dados do pagamento registrado

        Raises:
            ValueError: se houver erro na validação ou registro
            ConnectionError: se não conseguir conectar à API
        """
        return self.pagamento_repository.registrar_pagamento(
            pedido_id=pedido_id,
            forma_pagamento=forma_pagamento,
            valor_pago=valor_pago,
            status_pagamento="Confirmado",
            observacoes=observacoes,
        )

    def validar_valor_pagamento(self, pedido_id: int, valor_pago: float) -> bool:
        """
        Valida se o valor pago não excede o valor total do pedido.

        Args:
            pedido_id: ID do pedido
            valor_pago: Valor que será pago

        Returns:
            True se a validação foi bem-sucedida, False caso contrário

        Raises:
            ValueError: se houver erro na validação
            ConnectionError: se não conseguir conectar à API
        """
        resultado = self.pagamento_repository.validar_pedido_valor(
            pedido_id=pedido_id, valor_pago=valor_pago
        )
        return resultado.get("valido", False)
