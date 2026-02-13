from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.infrastructure.repository_client import ClienteRepositoryMemoria

class ClienteService:
    def __init__(self, repository):
        self.repository = repository

    def criar_cliente(self, dados):
        return self.repository.criar(dados)

    def listar_clientes(self):
        return self.repository.listar()

    def buscar_cliente(self, cliente_id):
        return self.repository.buscar_por_id(cliente_id)

# Instancia o service com repositório em memória
cliente_service = ClienteService(repository=ClienteRepositoryMemoria())
