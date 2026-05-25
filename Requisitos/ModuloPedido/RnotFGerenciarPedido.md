# Requisitos do Módulo order_form_list.py

## Objetivo
Criar uma tela em Python (Tkinter) que exibe em um **grid** todas as ordens solicitadas, permitindo ações de **cancelar** e **deletar** diretamente na interface.

---

## Endpoints da API

### Base
- `API_BASE = "http://localhost:8000/api/v1"`

### Listar Ordens
- **Endpoint**: `/v1/orders`
- **Retorno**:
  - `numero` (integer) → Número do pedido
  - `data_criacao` (date-time) → Data de criação
  - `cliente` (string) → Nome do cliente
  - `status` (string) → Status atual
  - `valor_total` (decimal) → Valor total do pedido
  - `observacoes` (string) → Observações
  - `itens` (array de OrderItem):
    - `produto`
    - `quantidade`
    - `preco_unitario`
    - `subtotal`
  - `historico_status` (array de OrderStatusHistory):
    - `data_hora`
    - `status_anterior`
    - `novo_status`
    - `usuario`
    - `observacoes`

### Buscar Ordem por ID
- **Endpoint**: `/v1/orders/{id}`
- Retorna os mesmos dados da listagem, filtrados por ID.

### Deletar Ordem
- **Endpoint**: `/v1/orders/{id}`
- Remove a ordem pelo identificador.

### Cancelar Ordem
- **Endpoint**: `/v1/orders/{id}/status`
- **Payload**:
  ```json
  {
    "status": "string",
    "usuario": "sistema",
    "observacoes": ""
  }
