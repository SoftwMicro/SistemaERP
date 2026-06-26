"""Repository para operações de comprovante - centraliza chamadas à API."""
import json
import os
import random
import string
import urllib.error
import urllib.request
from typing import Any, Dict


class ComprovanteRepository:
    """Gerencia chamadas à API de comprovante."""

    def __init__(self):
        self.base_url = os.getenv("FINANCEIRO_API_URL", "http://localhost:8080")

    def emitir_comprovante(
        self,
        pedido_id: int,
        tipo: str,
        numero_comprovante: str | None = None,
        data_emissao: str | None = None,
    ) -> Dict[str, Any]:
        """Emite um comprovante pela API.

        Args:
            pedido_id: ID do pedido
            tipo: Tipo do comprovante
            numero_comprovante: Número do comprovante (opcional)
            data_emissao: Data de emissão em ISO 8601 (opcional)

        Returns:
            Dicionário com a resposta da API.

        Raises:
            ValueError: Se a API retornar erro ou a resposta for inválida
            ConnectionError: Se não conseguir conectar à API
        """
        if not numero_comprovante:
            numero_comprovante = self._gerar_numero_comprovante()

        payload = {
            "orderId": pedido_id,
            "numeroComprovante": numero_comprovante,
            "tipo": tipo,
        }

        if data_emissao:
            payload["dataEmissao"] = data_emissao

        api_url = f"{self.base_url}/api/comprovantes/emitir"
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

    def _gerar_numero_comprovante(self) -> str:
        codigo = "".join(random.choices(string.digits, k=8))
        return f"RCPT-{codigo}"
