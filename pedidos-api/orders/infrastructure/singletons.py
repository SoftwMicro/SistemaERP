from orders.infrastructure.repository import ClienteRepositoryMemoria
from orders.infrastructure.repository_product import ProductRepositoryMemoria
from orders.infrastructure.repository_order import OrderRepositoryMemoria
from orders.application.client_service import ClienteService
from orders.application.product_service import ProductService
from orders.application.order_service import OrderService

cliente_repository = ClienteRepositoryMemoria()
product_repository = ProductRepositoryMemoria()
order_repository = OrderRepositoryMemoria()

cliente_service = ClienteService(repository=cliente_repository)
product_service = ProductService(repository=product_repository)
order_service = OrderService(order_repository, cliente_service, product_service)
