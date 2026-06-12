import requests


class PagamentoController:
    """Controller to fetch order data from orders API."""

    BASE_URL = "http://localhost:8000/api/v1/orders"

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
