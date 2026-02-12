# Requisito Funcional - Módulo Pedidos

## Objetivo
Criar o módulo **Pedidos** no projeto Django, seguindo arquitetura limpa (Domain, Application, Infrastructure) e boas práticas já utilizadas nos módulos anteriores.

## Estrutura de pastas e arquivos
Dentro do app `orders/` criar:

- `domain/order.py` → Entidade Pedido (número único, data/hora, cliente, status, valor total, observações).
- `domain/order_item.py` → Entidade Item do Pedido (produto, quantidade, preço unitário, subtotal).
- `domain/order_status_history.py` → Entidade Histórico de Status (data/hora, status anterior, novo status, usuário responsável, observações).
- `application/order_service.py` → Casos de uso (criar pedido, listar pedidos, obter pedido, alterar status, cancelar pedido).
- `infrastructure/repository_order.py` → Repositório em memória para Pedido.
- `infrastructure/views_order.py` → Views DRF para expor endpoints.
- Atualizar `orders/urls.py` → incluir rotas de pedidos.

## Requisitos funcionais
- **POST** `/api/v1/orders` → Criar pedido
- **GET** `/api/v1/orders` → Listar pedidos
- **GET** `/api/v1/orders/:id` → Obter pedido
- **PATCH** `/api/v1/orders/:id/status` → Alterar status
- **DELETE** `/api/v1/orders/:id` → Cancelar pedido

## Regras de negócio
- Número único do pedido gerado automaticamente.
- Data/hora de criação registrada no momento da criação.
- Pedido associado a um cliente existente.
- Status do pedido: `PENDENTE`, `CONFIRMADO`, `SEPARADO`, `ENVIADO`, `ENTREGUE`, `CANCELADO`.
- Valor total calculado a partir dos itens.
- Observações opcionais.
- Itens do pedido devem registrar produto, quantidade, preço unitário no momento da criação e calcular subtotal.
- Histórico de status deve registrar todas as mudanças com data/hora, status anterior, novo status, usuário responsável e observações.

## Boas práticas
- Seguir arquitetura limpa (Domain, Application, Infrastructure).
- Cada camada com responsabilidade única.
- Views chamam apenas o service da camada Application.
- Service depende de abstrações (repository).
- Repository em memória implementa persistência mockada.
- Retorno sempre em JSON via DRF.