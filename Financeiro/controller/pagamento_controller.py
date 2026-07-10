import logging

import requests

from ..auth_context import get_current_user
from ..repository.pagamento_repository import PagamentoRepository

logger = logging.getLogger(__name__)


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
        Registra um novo pagamento e atualiza o status do pedido.

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
        pagamento_response = self.pagamento_repository.registrar_pagamento(
            pedido_id=pedido_id,
            forma_pagamento=forma_pagamento,
            valor_pago=valor_pago,
            status_pagamento="Confirmado",
            observacoes=observacoes,
        )

        usuario = get_current_user()
        usuario_identificacao = (
            str(usuario.login)
            if usuario and getattr(usuario, "login", None)
            else str(usuario.id) if usuario and getattr(usuario, "id", None) is not None else "sistema"
        )

        observacoes_status = "Pagamento realizado"
        if pagamento_response and isinstance(pagamento_response, dict):
            codigo_evento = (
                pagamento_response.get("codigo")
                or pagamento_response.get("transactionCode")
                or pagamento_response.get("id")
                or pagamento_response.get("orderId")
            )
            if codigo_evento is not None:
                observacoes_status = f"Pagamento realizado. Código da transação: {codigo_evento}"

        status_url = f"{self.BASE_URL}/{pedido_id}/status"
        payload = {
            "status": "CONFIRMADO",
            "usuario": usuario_identificacao,
            "observacoes": observacoes_status,
        }

        try:
            response = requests.patch(status_url, json=payload, timeout=10)
            if response.status_code not in (200, 201):
                logger.error(
                    "Falha ao atualizar status do pedido %s: %s %s",
                    pedido_id,
                    response.status_code,
                    response.text,
                )
                raise ValueError(
                    f"Falha ao atualizar status do pedido: {response.status_code} {response.text}"
                )
        except requests.RequestException as exc:
            logger.error(
                "Erro de conexão ao atualizar status do pedido %s: %s",
                pedido_id,
                exc,
                exc_info=True,
            )
            raise ConnectionError(
                f"Não foi possível atualizar o status do pedido: {exc}"
            ) from exc

        return pagamento_response

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
