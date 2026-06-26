### 3.5 Comprovantes
- Emitir comprovante por numero do pedido.
- Ao emetir Usuario informara o numero do pedido
- Usuario selecionara o tipo, Fiscal Nao fiscal
- Aplicacao gerara numero_comprovante aleatoriio para montar Json de envio
- Comunicacao via Api
-@RequestMapping("/api/comprovantes/emitir")
ReceiptRequest {
Long orderId;
String numeroComprovante;
String tipo;
LocalDateTime dataEmissao;

 public ResponseEntity<?> emitReceipt(@RequestBody ReceiptRequest request)


- A Receber a resposta da Api montar o comprovante com dados e modelo abaixo:

Comportamento esperado exemplo
Requisição POST /api/comprovantes/emitir com corpo: { "orderId": 1, "numeroComprovante": "RCPT-xxx", // opcional, se não informado é gerado "tipo": "Fiscal", // por ex. "dataEmissao": "2026-06-25T19:34:00" // opcional }
Se pedido não existir -> 400 Bad Request: "Pedido não existe: {id}"
Se não existir pagamento para o pedido -> 400 Bad Request: "Não existe pagamento para o pedido informado: {id}"
Se existir pagamento -> 201 Created com corpo JSON: { "receipt": { /* OrdersReceipt persistido: id, orderId, numeroComprovante, tipo, dataEmissao */ }, "rows": [ { "pedidoId": 1, "quantidade": 2, "precoUnitario": 10.00, "subtotal": 20.00, "sku": "ABC-123", "nomeProduto": "Nome do produto", "formaPagamento": "CARTAO", "valorPago": 20.00, "dataPagamento": "25/06/2026 19:34", // formato DATE_FORMAT do SQL usado "statusPagamento": "CONFIRMADO", "totalGeral": 100.00 }, ... ] }

- Gerar comprovante abaixo em uma tela.
============================================================
                      NOME DA EMPRESA                       
                 CNPJ: 00.000.000/0001-00                   
             Rua dos Desenvolvedores, 1024 - TI            
============================================================
              EXTRATO No. [pedido_id]                      
                  CUPOM FISCAL ELETRÔNICO                   
============================================================
# | COD | DESCRIÇÃO | QTD | UN | VL UN R$ | (VL TRB R$)*| VL ITEM R$
------------------------------------------------------------
[item_num] [sku] - [nome_produto]
               [quantidade] UN X R$ [preco_unitario] -> R$ [subtotal]
------------------------------------------------------------
TOTAL BRUTO R$                                     [total_geral]
------------------------------------------------------------
FORMA DE PAGAMENTO                                 VALOR PAGO R$
[forma_pagamento]                                  R$ [valor_pago]
------------------------------------------------------------
Status do Pagamento: [status_pagamento]
============================================================
          OBRIGADO PELA PREFERENCIA - VOLTE SEMPRE          
============================================================




Api --- Manutencao

- prompts: #file:OrdersReceiptController.java Ao emitReceipt o sistema verificara se existe pagamento para orderId, caso nao existir emitir mensagem que nao existe pagamento para o pedido informado.
- Gerar comprovantes com dados do pedido item e pedido pagamento e produto.
- Caso existir montar o comprovante com dados para response da query abaixo:

-- definição query para response

SELECT 
    -- Dados do Pedido / Item
    oi.pedido_id,
    oi.quantidade,
    oi.preco_unitario,
    oi.subtotal,
    
    -- Dados do Produto (Novidade)
    p.sku,
    p.nome AS nome_produto,
    
    -- Dados do Pagamento
    pag.forma_pagamento,
    pag.valor_pago,
    DATE_FORMAT(pag.data_pagamento, '%d/%m/%Y %H:%i') AS data_pagamento,
    pag.status_pagamento,
    
    -- Totalizador Geral do Pedido
    SUM(oi.subtotal) OVER(PARTITION BY oi.pedido_id) AS total_geral
FROM 
    orders_orderitem oi
INNER JOIN 
    orders_produto p ON oi.produto_id = p.id
LEFT JOIN 
    orders_pagamento pag ON oi.pedido_id = pag.order_id
WHERE 
    oi.pedido_id = 1; -- Substitua pelo ID do pedido que deseja imprimir
