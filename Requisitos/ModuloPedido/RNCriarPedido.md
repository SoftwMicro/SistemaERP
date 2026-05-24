# Fluxo de Execução - Criar Pedido

## Checklist Passo a Passo

1. **Verificar Idempotência**
   - Existe `idempotency_key`?
   - Se sim, buscar pedido associado.
   - Se pedido já existe → retornar pedido e encerrar.

2. **Validar Cliente**
   - Buscar cliente pelo `cliente_id`.
   - Cliente não encontrado → erro.
   - Cliente inativo → erro.

3. **Validar Itens**
   - Lista de itens existe?
   - Cada item possui quantidade > 0?
   - Se não → erro.

4. **Controle de Concorrência e Estoque**
   - Para cada item:
     - Produto existe?
     - Produto ativo?
     - Tentar adquirir lock no SKU via Redis.
       - Se lock não disponível → erro de concorrência.
     - Verificar estoque atual.
       - Se quantidade solicitada > estoque disponível → erro.
     - Guardar informações do produto para reserva.

   - Se ocorrer erro em qualquer item:
     - Liberar todos os locks adquiridos.
     - Encerrar com erro.

5. **Reserva de Estoque**
   - Atualizar estoque de cada produto (subtrair quantidade solicitada).
   - Criar lista de itens (`OrderItem`) com SKU, quantidade e preço unitário.

6. **Criar Pedido**
   - Instanciar objeto `Order` com cliente, itens e observações.
   - Associar `idempotency_key` ao pedido.
   - Salvar pedido no repositório.

7. **Persistência de Idempotência**
   - Se houver `idempotency_key`, salvar chave no Redis vinculada ao número do pedido.

8. **Liberação de Locks**
   - Liberar todos os locks de SKU adquiridos.

9. **Retorno**
   - Retornar pedido criado com sucesso.
