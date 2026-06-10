"""Repository para operações de caixa - centraliza chamadas à API."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import List, Dict, Any


class CaixaRepository:
    """Gerencia chamadas à API de operações de caixa."""

    def __init__(self):
        self.base_url = os.getenv("FINANCEIRO_API_URL", "http://localhost:8080")

    def abrir_caixa(self, usuario_id: int, saldo_inicial: float) -> Dict[str, Any]:
        """
        Abre um novo caixa.

        Args:
            usuario_id: ID do usuário
            saldo_inicial: Saldo inicial do caixa

        Returns:
            Dict com os dados do caixa aberto

        Raises:
            ValueError: Se houver erro na requisição
            ConnectionError: Se não conseguir conectar à API
        """
        api_url = f"{self.base_url}/caixa/abrir"
        form = {
            "usuarioId": str(usuario_id),
            "saldoInicial": str(saldo_inicial),
        }
        data = urllib.parse.urlencode(form).encode("utf-8")
        request = urllib.request.Request(
            api_url,
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
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

    def fechar_caixa(self, caixa_id: int, saldo_final: float) -> Dict[str, Any]:
        """Fecha o caixa com o saldo final informado."""
        api_url = f"{self.base_url}/caixa/fechar/{caixa_id}"
        params = urllib.parse.urlencode({"saldoFinal": str(saldo_final)})
        full_url = f"{api_url}?{params}"

        request = urllib.request.Request(
            full_url,
            headers={
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

    def obter_aberturas_fechamentos(self, usuario_id: int) -> List[Dict[str, Any]]:
        """
        Obtém a lista de aberturas e fechamentos de caixa do usuário.

        Args:
            usuario_id: ID do usuário

        Returns:
            Lista de dicionários com os dados das aberturas

        Raises:
            ValueError: Se houver erro na requisição
            ConnectionError: Se não conseguir conectar à API
        """
        api_url = f"{self.base_url}/caixa/obter-abertura-fechamento"
        params = urllib.parse.urlencode({"usuarioId": usuario_id})
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
                data = json.loads(body)
                # Garante que sempre retorna uma lista
                return data if isinstance(data, list) else []
        except urllib.error.HTTPError as error:
            if error.code == 404:
                # Retorna lista vazia se não encontrar
                return []
            error_body = error.read().decode("utf-8", errors="ignore").strip()
            details = error_body or str(error.reason) or "Sem corpo de erro"
            raise ValueError(
                f"API retornou erro {error.code} {error.reason}: {details}"
            ) from error
        except urllib.error.URLError as error:
            raise ConnectionError(f"Não foi possível acessar a API: {error.reason}") from error
        except json.JSONDecodeError as error:
            raise ValueError(f"Resposta da API inválida: {body}") from error
