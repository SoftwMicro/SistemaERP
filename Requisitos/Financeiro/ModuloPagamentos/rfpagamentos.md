# Especificação de Desenvolvimento - Registro de Pagamento

## 1. Objetivo
Acoplar funcionalidade de **Registro de Pagamento** na aplicação desktop em Python (Tkinter), seguindo arquitetura **MVC** já existente.  
A tela permitirá:
- Seleção de forma de pagamento (Dinheiro, Cartão, Pix).
- Inserção do valor pago.
- comunicação com end point interface

valores entrada

POST
Example Value
Schema
{
  "orderId": 0,
  "formaPagamento": "string",
  "valorPago": 0,
  "dataPagamento": "2026-06-12T00:38:41.149Z",
  "statusPagamento": "string"
}

- End point
http://localhost:8080/api/pagamentos/registrarPagamentos

- Confirmação da operação.

## 2. Fluxo de Operação atual para reajustar e acoplar

1. **Seleção de Pedido**
   - Usuário informa o **ID do pedido**.
   - Sistema consulta API ou base de dados para validar existência do pedido.
   - Exibe dados do pedido na tela.

2. **Registro de Pagamento**
   - Usuário seleciona forma de pagamento:
     - Dinheiro
     - Cartão
     - Pix
   - Informa valor pago.
   - Clica em **Confirmar Pagamento**.


## 3. Formulário de Pagamento

- **Campos obrigatórios:**
  - Seleção de forma de pagamento (combobox).
  - Campo para valor pago (entrada formatada em moeda brasileira).
- **Botões:**
  - **Confirmar Pagamento** → se comunicar com Api.
- **Feedback:**
  - Mensagem de sucesso (verde).
  - Mensagem de erro (vermelho).

---

## 4. Requisitos Funcionais

- Validação de pedido existente antes de registrar pagamento.
- Valor pago não pode ser maior que `valor_total` do pedido.
  - Formulário simples para pagamento.
  - Feedback visual imediato.

---

## 5. Padrão Arquitetural (MVC)

- **Model**:
- **View**:
    - Formulário de pagamento.
    - Botão Confirmar.
- **Controller**:
  - Persistência do pagamento.
  - Atualização de status e histórico.
  - Mensagens de feedback para o usuário.

## 6 - Observações
 - A tela de pedidos e - Usuário informa o **ID do pedido**. já pronta
 - Sistema consulta API ou base de dados para validar existência do pedido. já pronto.
