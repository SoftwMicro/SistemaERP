from ..repository.comprovante_repository import ComprovanteRepository


class ComprovanteController:
    """Controller para gerenciar a emissão de comprovantes."""

    def __init__(self):
        self.repository = ComprovanteRepository()

    def emitir_comprovante(
        self,
        pedido_id: int,
        tipo: str,
        numero_comprovante: str | None = None,
        data_emissao: str | None = None,
    ) -> dict:
        """Emite um comprovante através da API.

        Args:
            pedido_id: ID do pedido
            tipo: Tipo do comprovante
            numero_comprovante: Número do comprovante (opcional)
            data_emissao: Data de emissão em ISO 8601 (opcional)

        Returns:
            Dicionário com os dados retornados pela API.

        Raises:
            ValueError: Se os dados fornecidos forem inválidos ou ocorrer erro na API
            ConnectionError: Se não for possível conectar à API
        """
        if not pedido_id or pedido_id <= 0:
            raise ValueError("Informe um ID de pedido válido.")

        tipo_formatado = str(tipo).strip()
        if not tipo_formatado:
            raise ValueError("Informe o tipo de comprovante.")

        return self.repository.emitir_comprovante(
            pedido_id=pedido_id,
            tipo=tipo_formatado,
            numero_comprovante=numero_comprovante,
            data_emissao=data_emissao,
        )
