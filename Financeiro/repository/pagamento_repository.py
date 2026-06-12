"""Repository para operações de pagamento - centraliza chamadas à API."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Any


class PagamentoRepository:
    """Gerencia chamadas à API de pagamentos."""

    def __init__(self):
        self.base_url = os.getenv("FINANCEIRO_API_URL", "http://localhost:8080")

    def registrar_pagamento(
        self,
        pedido_id: int,
        forma_pagamento: str,
        valor_pago: float,
        status_pagamento: str = "Confirmado",
        observacoes: str | None = None,
    ) -> Dict[str, Any]:
        """
        Registra um novo pagamento na API.

        Args:
            pedido_id: ID do pedido
            forma_pagamento: Forma de pagamento (Dinheiro, Cartão, Pix)
            valor_pago: Valor do pagamento
            status_pagamento: Status do pagamento (padrão: Confirmado)
            observacoes: Observações opcionais

        Returns:
            Dicionário com os dados do pagamento registrado

        Raises:
            ValueError: Se houver erro na requisição
            ConnectionError: Se não conseguir conectar à API
        """
        api_url = f"{self.base_url}/api/pagamentos/registrarPagamentos"

        payload = {
            "orderId": pedido_id,
            "formaPagamento": forma_pagamento,
            "valorPago": valor_pago,
            "statusPagamento": status_pagamento,
        }

        if observacoes:
            payload["observacoes"] = observacoes

        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            api_url,
            data=data,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                body = response.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as error:
            error_body = error.read().decode("utf-8", errors="ignore").strip()
            details = error_body or str(error.reason) or "Sem corpo de erro"
            raise ValueError(
                f"API retornou erro {error.code} {error.reason}: {details}"
            ) from error
        except urllib.error.URLError as error:
            raise ConnectionError(f"Não foi possível acessar a API: {error.reason}") from error
        except json.JSONDecodeError as error:
            raise ValueError(f"Resposta da API inválida: {body}") from error

    def validar_pedido_valor(self, pedido_id: int, valor_pago: float) -> Dict[str, Any]:
        """
        Valida se o valor pago não excede o valor total do pedido.

        Args:
            pedido_id: ID do pedido
            valor_pago: Valor que será pago

        Returns:
            Dicionário com resultado da validação

        Raises:
            ValueError: Se houver erro na validação
            ConnectionError: Se não conseguir conectar à API
        """
        api_url = f"{self.base_url}/api/pagamentos/validar-valor"
        params = urllib.parse.urlencode(
            {"orderId": str(pedido_id), "valorPago": str(valor_pago)}
        )
        full_url = f"{api_url}?{params}"

        request = urllib.request.Request(
            full_url,
            headers={
                "Accept": "application/json",
            },
            method="GET",
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                body = response.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as error:
            error_body = error.read().decode("utf-8", errors="ignore").strip()
            details = error_body or str(error.reason) or "Sem corpo de erro"
            raise ValueError(
                f"API retornou erro {error.code} {error.reason}: {details}"
            ) from error
        except urllib.error.URLError as error:
            raise ConnectionError(f"Não foi possível acessar a API: {error.reason}") from error
        except json.JSONDecodeError as error:
            raise ValueError(f"Resposta da API inválida: {body}") from error
