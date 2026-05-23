# Requisitos do Módulo order_form.py

## Objetivo
Criar um formulário em Python (Tkinter) para solicitação de pedidos, permitindo selecionar um cliente e múltiplos produtos antes de enviar o pedido para a API.

## Fluxo de Funcionalidade

1. **Pesquisa de Cliente**
   - O usuário poderá pesquisar o cliente pelo **ID**.
   - Ao realizar a pesquisa, os dados do cliente serão exibidos em um **grid**.
   - O usuário deverá selecionar o cliente desejado no grid.

2. **Seleção de Produtos**
   - O sistema deve listar todos os produtos disponíveis.
   - Os produtos serão exibidos em um **grid**.
   - O usuário poderá selecionar **um ou mais produtos** para compor o pedido.

3. **Validação para Realizar Pedido**
   - O pedido só poderá ser realizado se:
     - Um cliente estiver selecionado.
     - Pelo menos **1 produto** estiver selecionado.
   - O usuário poderá selecionar múltiplos produtos.

4. **Finalização do Pedido**
   - Após selecionar cliente e produtos, o usuário clicará no botão **Realizar Pedido**.
   - Exibir mensagem: **"Pedido realizado com sucesso"** após confirmação da API.

---

## Endpoints da API

### Base
- `API_BASE = "http://localhost:8000/api/v1"`

### Cliente
- **Obter Cliente por ID**  
  - Endpoint: `/customers/{id}`  
  - Retorno:  
    - `id` (integer, readOnly)  
    - `nome` (string, obrigatório, maxLength 100)  
    - `cpf_cnpj` (string, obrigatório, maxLength 18)  
    - `email` (string, obrigatório, maxLength 254, formato email)  
    - `telefone` (string, obrigatório, maxLength 20)  
    - `endereco` (string, obrigatório)  

### Produtos
- **Listar Produtos**  
  - Endpoint: `/products`  
  - Retorno (lista de objetos Produto):  
    - `sku` (string, obrigatório, maxLength 30)  
    - `nome` (string, obrigatório, maxLength 100)  
    - `descricao` (string, obrigatório)  
    - `preco` (decimal, obrigatório)  
    - `quantidade_estoque` (integer, obrigatório)  
    - `ativo` (boolean, default true)  

### Pedido
- **Solicitar Pedido (POST)**  
  - Endpoint: `/orders`  
  - Payload esperado:  
    - `cliente` (integer, ID do cliente)  
    - `itens` (array de objetos)  
      - `produto` (referência ao produto selecionado)  
      - `quantidade` (quantidade solicitada)  
    - `observacoes` (string, opcional)

---

## Requisitos Funcionais
- Grid para exibir dados do cliente pesquisado.
- Grid para listar produtos disponíveis.
- Seleção múltipla de produtos.
- Botão **Realizar Pedido**:
  - Exibir loading enquanto aguarda resposta.
  - Desabilitar botão até receber retorno da API.
  - Exibir mensagem de sucesso após confirmação.

## Observações
- O módulo deve seguir padrão **MVC**.
- O comportamento do botão deve ser consistente com os módulos anteriores (`produto_form.py` e `cliente_form.py`).
