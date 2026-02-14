# 7. Problema e Solução de Concorrência com Redis

## 7.1 Problema Identificado
- **Cenário:** Produto X tem 10 unidades em estoque. Dois pedidos simultâneos tentam comprar 8 unidades cada.
- **Resultado observado:** Ambos os pedidos retornaram erro **400** (nenhum foi aceito).
- **Causa:** A lógica de reserva de estoque não está protegida contra **condições de corrida (race condition)**.  
  Ambos os processos verificam o estoque como suficiente antes de reservar, mas falham ao tentar atualizar simultaneamente.

---

## 7.2 Solução com Redis

### Locks Distribuídos
- Utilizar **Redis** para implementar um **lock por produto** durante a operação de reserva de estoque.
- Exemplo de chave de lock: `lock:produto:{sku}`.
- Apenas um processo pode adquirir o lock por vez.  
  - Se o lock estiver ocupado, o segundo processo deve aguardar ou falhar com erro de estoque insuficiente.

### Idempotência
- Usar Redis para armazenar a chave `idempotency_key` fornecida pelo cliente:
  - `idempotency:{idempotency_key} -> pedido_id`.
- Se a mesma requisição for recebida novamente, retornar o pedido já criado em vez de duplicar.

### Atomicidade
- Utilizar **transações Redis (MULTI/EXEC)** ou **scripts Lua** para garantir que múltiplas reservas de estoque sejam feitas de forma atômica:
  - Se qualquer item não tiver estoque suficiente, a transação é abortada.
  - Nenhum estoque é reservado parcialmente.

---

## 7.3 Fluxo da Reserva de Estoque com Redis

1. **Aquisição de Lock**
   - `SETNX lock:produto:{sku} <pedido_id> EX 5`
   - Se não conseguir adquirir o lock, retornar erro de concorrência.

2. **Validação de Estoque**
   - Ler quantidade disponível do produto.
   - Se suficiente, reservar (decrementar).
   - Se insuficiente, liberar lock e retornar erro.

3. **Confirmação**
   - Persistir pedido no banco de dados.
   - Liberar lock (`DEL lock:produto:{sku}`).

4. **Idempotência**
   - Antes de criar o pedido, verificar se existe chave `idempotency:{idempotency_key}`.
   - Se existir, retornar pedido já criado.
   - Se não existir, criar pedido e salvar chave no Redis.

---

## 7.4 Benefícios
- **Concorrência controlada:** apenas um processo pode reservar estoque por produto.
- **Idempotência garantida:** evita duplicação de pedidos em caso de retries.
- **Atomicidade:** pedidos com múltiplos itens são tratados como transação única (tudo ou nada).
- **Performance:** Redis é extremamente rápido e adequado para operações de alta concorrência.

---

## 7.5 Próximos Passos
- Implementar integração com Redis no projeto Django (`django-redis`).
- Criar camada de serviço para gerenciar locks e idempotência.
- Escrever testes automatizados que simulam concorrência e retries para validar a solução.