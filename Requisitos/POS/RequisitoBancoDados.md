# Entidades de Banco de Dados - POS

## Já Existentes
- **Orders** → Pedido principal.
- **OrderItems** → Itens do pedido.
- **Estoques** → Controle de estoque.
- **Histórico de Status** → Auditoria de mudanças de status.

## Entidades Complementares Necessárias

### 1. Pagamentos
- Registra como o pedido foi pago.
- Atributos principais:
  - Id
  - OrderId (FK → Orders)
  - FormaPagamento (Dinheiro, Cartão, Pix, etc.)
  - ValorPago
  - DataPagamento
  - StatusPagamento (Aprovado, Pendente, Cancelado)

### 2. Caixa (CashRegister)
- Representa o ponto de venda físico ou sessão de caixa.
- Atributos principais:
  - Id
  - UsuarioId (FK → Usuários do sistema)
  - DataAbertura
  - DataFechamento
  - SaldoInicial
  - SaldoFinal
  - Status (Aberto, Fechado)

### 3. Usuários (Operators)
- Quem opera o POS.
- Atributos principais:
  - Id
  - Nome
  - Login
  - Senha (hash)
  - Perfil (Caixa, Gerente, Admin)
  - Ativo

### 4. Receipts (Comprovantes)
- Armazena informações do comprovante fiscal ou não fiscal.
- Atributos principais:
  - Id
  - OrderId (FK → Orders)
  - NumeroComprovante
  - Tipo (Fiscal, Não Fiscal)
  - DataEmissao

---

## Observações
- **Orders + OrderItems + Estoques + Histórico de Status** já cobrem a parte de pedidos e estoque.
- **Pagamentos** é essencial para registrar como a venda foi liquidada.
- **Caixa** permite controlar abertura/fechamento e conciliação de valores.
- **Usuários** garantem rastreabilidade de quem realizou a operação.
- **Receipts** permitem integração com emissão de comprovantes ou notas fiscais.

---

## Fluxo de Persistência no POS
1. Cliente selecionado → vinculado ao **Order**.
2. Produtos adicionados → registrados em **OrderItems** e descontados de **Estoques**.
3. Pedido criado → registrado em **Orders** e acompanhado em **Histórico de Status**.
4. Pagamento realizado → persistido em **Pagamentos**.
5. Operador do caixa → vinculado ao **Caixa** e ao **Order**.
6. Comprovante emitido → registrado em **Receipts**.
