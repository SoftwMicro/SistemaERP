# Testes Unitários - Módulo Pedidos

## Objetivo
Criar testes unitários mockados para validar o fluxo completo da API em memória, garantindo que as regras de negócio críticas sejam respeitadas.  
Os testes devem ser organizados em uma pasta separada (`tests/`) e seguir a arquitetura limpa (Domain, Application, Infrastructure).

## Estrutura de testes
Criar dentro do projeto:
- `tests/domain/test_order.py` → Testes das entidades (Pedido, Item, Histórico de Status).
- `tests/application/test_order_service.py` → Testes dos casos de uso (criar pedido, listar, obter, alterar status, cancelar).
- `tests/infrastructure/test_views_order.py` → Testes das views DRF simulando chamadas HTTP.

## Biblioteca de testes
- Utilizar **pytest** como framework principal.
- Utilizar **pytest-django** para integração com Django.
- Utilizar **requests** ou **APIClient** do DRF para simular chamadas HTTP.

## Fluxo a ser coberto
1. **Criar Cliente** → POST `/api/v1/customers`
   - Deve retornar cliente criado com ID.
2. **Criar Produto** → POST `/api/v1/products`
   - Deve retornar produto criado com SKU e estoque inicial.
3. **Criar Pedido** → POST `/api/v1/orders`
   - Deve reservar estoque atomicamente.
   - Se não houver estoque suficiente, deve rejeitar o pedido.
4. **Listar Pedidos** → GET `/api/v1/orders`
   - Deve retornar lista com pedidos criados.
5. **Obter Pedido** → GET `/api/v1/orders/:id`
   - Deve retornar detalhes do pedido, itens e histórico.
6. **Alterar Status** → PATCH `/api/v1/orders/:id/status`
   - Deve validar transições de status.
   - Deve registrar histórico de status.
7. **Cancelar Pedido** → DELETE `/api/v1/orders/:id`
   - Deve devolver estoque ao produto.
   - Deve registrar histórico de status.

## Regras de negócio a validar
- Estoque reservado atomicamente (tudo ou nada).
- Cancelamento devolve estoque.
- Transições inválidas de status devem ser rejeitadas.
- Histórico de status deve ser registrado em cada mudança.

## Boas práticas
- Testes independentes e isolados.
- Mockar repositório em memória.
- Garantir cobertura mínima de 80% do fluxo.
- Retorno sempre validado em JSON.