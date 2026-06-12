# Especificação de Desenvolvimento - Tela de Pagamentos

## 1. Objetivo
Desenvolver uma nova tela **Registar Pagamento** na aplicação desktop em Python (Tkinter), seguindo arquitetura **MVC** já existente.  
A tela permitirá:
- Seleção de pedido existente via **ID**.
- Exibição dos dados completos do pedido total e sub total.


## 2. Integração com API
- **Endpoint**: `http://localhost:8000/v1/orders/{id}`
- **Método**: GET
- **Uso**: Obter dados do pedido pelo ID informado pelo usuário.

### Exemplo de Retorno (Order)
```json
{
  "numero": 123,
  "data_criacao": "2026-06-11T19:00:00",
  "cliente": "João da Silva",
  "status": "ABERTO",
  "valor_total": "450.50",
  "observacoes": "Entrega rápida",
  "itens": [
    {
      "produto": "Notebook",
      "quantidade": 1,
      "preco_unitario": 450.50,
      "subtotal": 450.50
    }
  ],
  "historico_status": [
    {
      "data_hora": "2026-06-11T19:10:00",
      "status_anterior": "NOVO",
      "novo_status": "CONFIRMADO",
      "usuario": "sistema",
      "observacoes": ""
    }
  ]
}


3. Fluxo de Operação
Pesquisa de Pedido

Usuário informa o ID do pedido.

Ao clicar em Pesquisar, o sistema consulta a API.

Exibir dados do pedido em grid:

Número

Data de criação

Cliente

Status

Valor total

Observações

Itens (produto, quantidade, preço unitário, subtotal)

Histórico de status