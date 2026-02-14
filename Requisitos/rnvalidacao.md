## 5.2 Validações
- **Cliente**
  - Deve existir no sistema.
  - Deve estar ativo para que o pedido seja aceito.

- **Produtos**
  - Devem existir no catálogo.
  - Devem estar ativos (disponíveis para venda).

- **Itens do Pedido**
  - A quantidade de itens deve ser maior que zero.
  - O preço unitário deve corresponder ao preço atual do produto no momento da criação do pedido.

---

## 5.3 Idempotência
- A criação de pedidos deve ser **idempotente**.
- O cliente deve fornecer um campo **idempotency_key** único por requisição.
- Se uma requisição com a mesma chave for recebida novamente:
  - O sistema deve **retornar o pedido existente**.
  - **Não deve criar um pedido duplicado**.

---

## Observações Gerais
- Todas as operações devem ser **transacionais**, garantindo consistência dos dados.
- As regras devem ser cobertas por **testes automatizados** para assegurar integridade e evitar regressões.
- A idempotência protege contra duplicação de pedidos em cenários de falha de rede ou reenvio de requisições.
