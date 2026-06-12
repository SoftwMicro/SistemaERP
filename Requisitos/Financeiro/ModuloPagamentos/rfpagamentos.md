# Especificação de Desenvolvimento - Registro de Pagamento

## 1. Objetivo
Implementar funcionalidade de **Registro de Pagamento** na aplicação desktop em Python (Tkinter), seguindo arquitetura **MVC** já existente.  
A tela permitirá:
- Seleção de forma de pagamento (Dinheiro, Cartão, Pix).
- Inserção do valor pago.
- Confirmação da operação.
- Persistência em banco de dados (`orders_pagamento`).
- Atualização automática do status do pedido (`orders_order`).
- Registro da mudança em histórico (`orders_orderstatushistory`).

---

## 2. Fluxo de Operação

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
   - Inserir registro em `orders_pagamento`:
     - `order_id`
     - `forma_pagamento`
     - `valor_pago`
     - `data_pagamento`
     - `status_pagamento`

3. **Atualização de Status**
   - Após pagamento, atualizar status do pedido em `orders_order`.
   - Inserir registro em `orders_orderstatushistory`:
     - `data_hora`
     - `status_anterior`
     - `novo_status`
     - `usuario`
     - `observacoes`

---

## 3. Formulário de Pagamento

- **Campos obrigatórios:**
  - Seleção de forma de pagamento (combobox).
  - Campo para valor pago (entrada formatada em moeda brasileira).
- **Botões:**
  - **Confirmar Pagamento** → grava dados e atualiza status.
- **Feedback:**
  - Mensagem de sucesso (verde).
  - Mensagem de erro (vermelho).

---

## 4. Requisitos Funcionais

- Validação de pedido existente antes de registrar pagamento.
- Valor pago não pode ser maior que `valor_total` do pedido.
- Atualização automática do status do pedido após pagamento.
- Registro em histórico de status para auditoria.
- Interface clara e responsiva:
  - Grid para exibir dados do pedido.
  - Formulário simples para pagamento.
  - Feedback visual imediato.

---

## 5. Padrão Arquitetural (MVC)

- **Model**:
  - Classe `Pagamento` para representar registros em `orders_pagamento`.
  - Métodos para inserir pagamento e atualizar status do pedido.
- **View**:
  - Tela em Tkinter com:
    - Campo de ID do pedido.
    - Grid de dados do pedido.
    - Formulário de pagamento.
    - Botão Confirmar.
- **Controller**:
  - Lógica para validar pedido.
  - Persistência do pagamento.
  - Atualização de status e histórico.
  - Mensagens de feedback para o usuário.

---

## 6. Observações
- Todas as operações devem ser transacionais (rollback em caso de erro).
- Senhas e usuários devem ser validados antes de permitir operação financeira.
- Botões devem ser desabilitados durante execução da operação.
- Mensagens de feedback devem ser claras e visíveis.
