# Requisitos do Módulo cliente_form.py

## Objetivo
Criar um formulário em Python (Tkinter) para realizar o cadastro de clientes e exibir os registros em um grid. O módulo deve seguir o padrão **MVC**.

## Estrutura de Dados
Modelo **Cliente** com os seguintes atributos:
- **nome***: string  
  - Título: Nome  
  - maxLength: 100  
  - minLength: 1  
- **cpf_cnpj***: string  
  - Título: Cpf cnpj  
  - maxLength: 18  
  - minLength: 1  
- **email***: string (formato email)  
  - Título: Email  
  - maxLength: 254  
  - minLength: 1  
- **telefone***: string  
  - Título: Telefone  
  - maxLength: 20  
  - minLength: 1  
- **endereco***: string  
  - Título: Endereco  
  - minLength: 1  
- **ativo**: boolean  
  - Título: Ativo  

(*) Campos obrigatórios.

## Endpoints da API
- **Cadastro de Cliente (POST)**  
  - URL: `http://localhost:8000/api/v1/customers`  
  - Payload: JSON com os dados do cliente.  
  - Exemplo: `resp = requests.post(f"{API_BASE}/customers", json=dados)`

- **Listagem de Clientes (GET)**  
  - URL: `http://localhost:8000/api/v1/customers`  
  - Retorna todos os clientes cadastrados.  
  - Exemplo: `resp = requests.get(f"{API_BASE}/customers")`

## Requisitos Funcionais
- O formulário deve permitir entrada dos dados conforme atributos definidos.
- Ao clicar no botão **Salvar**:
  - Exibir **loading**.
  - Desabilitar o botão até receber a resposta da API.
  - Após resposta, atualizar o grid com os dados cadastrados.
- O grid deve listar todos os clientes retornados pelo endpoint GET.
- Seguir o padrão **MVC**:
  - **Model**: Estrutura dos dados do cliente.
  - **View**: Interface gráfica em Tkinter.
  - **Controller**: Lógica de integração com a API e atualização do grid.

## Observações
- O comportamento do botão **Salvar** deve ser semelhante ao implementado em `produto_form.py`.
- Este documento serve como guia de especificação para implementação do código em Python.
