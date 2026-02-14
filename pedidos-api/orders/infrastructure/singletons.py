from orders.infrastructure.repository_client import ClienteRepository
from orders.infrastructure.repository_product import ProductRepository
from orders.infrastructure.repository_order import OrderRepository
from orders.application.client_service import ClienteService
from orders.application.product_service import ProductService
from orders.application.order_service import OrderService

cliente_repository = ClienteRepository()
product_repository = ProductRepository()
order_repository = OrderRepository()

cliente_service = ClienteService(repository=cliente_repository)
product_service = ProductService(repository=product_repository)
order_service = OrderService(order_repository, cliente_service, product_service)
