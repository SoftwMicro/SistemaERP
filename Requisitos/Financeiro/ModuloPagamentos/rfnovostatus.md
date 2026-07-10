# Requisito: Atualização de Status do Pedido Pós-Pagamento

## 🎯 Objetivo
Automatizar a atualização do status de um pedido para `CONFIRMADO` assim que a resposta de sucesso de um pagamento for processada, identificando o usuário logado que originou ou está contextualizado na ação.

---

## 🛠️ Detalhes do Endpoint Destino
* **URL:** `http://localhost:8000/api/v1/orders/{id}/status`
* **Método:** `PATCH` (ou `PUT`, ajuste conforme o padrão do seu projeto)
* **Payload (JSON):**
```json
{
  "status": "CONFIRMADO",
  "usuario": "[NOME_OU_ID_DO_USUARIO_LOGADO]",
  "observacoes": "Pagamento realizado. Código da transação: [CODIGO_DO_EVENTO]"
} 

## Onde Implementar (Instruções para o Copilot)
Para respeitar o **Clean Code** e a **Arquitetura Limpa** já existente no projeto, siga estes passos:

1. **Localize o Fluxo de Pagamento:** Busque no fluxo da aplicacao responsável por processar o retorno de sucesso do pagamento.
2. **Obtenha o Contexto do Usuário:** Recupere o usuário autenticado a partir do contexto de segurança da aplicação.
3. **Identifique o Bloco de Sucesso:** No ponto exato onde o pagamento for validado como **sucesso**, capture o `id` do pedido e o código de retorno do evento de pagamento para montar o payload. ## 

Regras de Negócio e Critérios de Aceite
Mapeamento do Payload:

status: Deve ser enviado o valor fixo "CONFIRMADO".

usuario: Deve obter dinamicamente a identificação (username ou ID) do usuário logado no sistema.

observacoes: Deve concatenar o texto "Pagamento realizado " + o código identificador retornado pelo evento de pagamento.

Resiliência (Clean Code): A requisição HTTP para o endpoint de pedidos deve ser envolvida em um bloco de tratamento de exceções (try/catch). Caso falhe, capture o erro e gere um log descritivo (logger.error) para garantir a rastreabilidade.