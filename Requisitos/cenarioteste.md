# 6. Cenários de Teste Obrigatórios

## 6.1 Concorrência de Estoque
**Cenário:**  
Produto X tem 10 unidades em estoque. Dois pedidos simultâneos tentam comprar 8 unidades cada.

**Resultado esperado:**  
Apenas um pedido deve ser aceito. O outro deve falhar com erro de estoque insuficiente.

**Teste:**  
Criar um teste automatizado que simule requisições paralelas para reservar estoque.

---

## 6.2 Idempotência
**Cenário:**  
Cliente envia a mesma requisição de criação de pedido 3 vezes (simula retry após timeout).

**Resultado esperado:**  
Apenas um pedido deve ser criado. As outras requisições devem retornar o mesmo pedido (status 200 ou 201), sem gerar duplicados.

**Teste:**  
Enviar 3 requisições `POST` idênticas (mesma `idempotency_key`) e validar que apenas um pedido é persistido.

---

## 6.3 Atomicidade em Falha Parcial
**Cenário:**  
Pedido com 3 itens. Item 1 e 2 têm estoque disponível, mas o Item 3 não tem.

**Resultado esperado:**  
O pedido deve falhar completamente. Nenhum estoque deve ser reservado.

**Teste:**  
Validar que o estoque dos itens 1 e 2 permanece inalterado após a falha do pedido.