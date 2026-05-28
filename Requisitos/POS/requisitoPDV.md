# Requisitos do Módulo POS (Ponto de Venda) aplicação desktop python

## Objetivo
Implementar um módulo de Ponto de Venda (POS) em python aplicação desktop que permita realizar vendas integrando diretamente as tabelas já existentes no banco de dados:  
- `orders_cliente`  
- `orders_produto`  
- `orders_order`  
- `orders_orderitem`  
- `orders_orderstatushistory`

---

## Pasta
Pos

## Fluxo de Operação

1. **Identificação do Cliente**
   - Usuário pesquisa cliente pelo CPF/CNPJ ou ID na tabela `orders_cliente`.
   - Exibir dados do cliente em um grid.
   - Cliente deve ser selecionado para prosseguir com a venda.
   - Validar se o cliente está ativo (`ativo = 1`).

2. **Seleção de Produtos**
   - Listar produtos disponíveis da tabela `orders_produto`.
   - Exibir atributos principais:
     - SKU
     - Nome
     - Preço
     - Quantidade em estoque
   - Usuário pode selecionar múltiplos produtos.
   - Validar se o produto está ativo (`ativo = 1`).
   - Validar estoque (`quantidade_estoque >= quantidade informada`).

3. **Carrinho de Compras**
   - Exibir grid com produtos selecionados:
     - Nome
     - Quantidade
     - Preço unitário
     - Subtotal
   - Atualizar automaticamente o **valor total da venda**.

4. **Finalização da Venda**
   - Só é possível finalizar se:
     - Um cliente estiver selecionado.
     - Pelo menos 1 produto estiver no carrinho.
   - Botão **Finalizar Pedido**:
     - Inserir registro em `orders_order`:
       - `data_criacao`
       - `status` inicial (ex.: "ABERTO")
       - `valor_total`
       - `observacoes`
       - `cliente_id`
     - Inserir itens em `orders_orderitem` vinculados ao pedido.
     - Atualizar estoque em `orders_produto` (subtrair quantidade vendida).
     - Inserir registro em `orders_orderstatushistory` com status inicial.

   - Exibir mensagem: **"Venda realizada com sucesso"**.

5. **Cancelamento ou Exclusão**
   - Cancelar pedido:
     - Atualizar `status` em `orders_order`.
     - Inserir registro em `orders_orderstatushistory` com status anterior e novo status.
   - Deletar pedido:
     - Remover registros de `orders_orderitem` vinculados.
     - Remover registro de `orders_order`.
     - Atualizar estoque em `orders_produto` (repor quantidade).
   - Atualizar grid após operação.

---

## Requisitos Funcionais

- Grid para exibir clientes pesquisados diretamente da tabela `orders_cliente`.
- Grid para listar produtos disponíveis da tabela `orders_produto`.
- Grid para carrinho de compras com cálculo automático de subtotal e total.
- Botão **Finalizar Pedido** com loading e desabilitado até conclusão da transação no banco.
- Botões de ação:
  - **Cancelar Pedido** (update em `orders_order` + log em `orders_orderstatushistory`).
  - **Deletar Pedido** (delete em `orders_order` + `orders_orderitem`).
- Mensagens de feedback claras:
  - Sucesso (verde).
  - Erro (vermelho).
- Atualização automática do grid após qualquer operação.

---

## Padrão Arquitetural
- Seguir padrão **MVC**:
  - **Model**: Estrutura de Cliente, Produto, Pedido, Itens e Histórico.
  - **View**: Interface gráfica em Tkinter com grids e botões.
  - **Controller**: Lógica de integração com o banco de dados e atualização da interface.

---

## Observações
- Todas as operações devem ser transacionais:
  - Se ocorrer erro, aplicar rollback.
- Botões devem ser desabilitados enquanto aguardam execução da transação.
- Em caso de erro, exibir mensagem clara e não alterar o estado atual da tela.

## conexão banco de dados
        'NAME': 'pedidos',
        'USER': 'admin',
        'PASSWORD': '010101',
        'HOST': 'localhost',
        'PORT': '3306'
