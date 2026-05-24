# Tela de Dashboard

## Objetivo
Criar uma tela de **Dashboard** que ocupa todo o espaço da janela principal e contém um menu de navegação para os módulos do sistema.

## Estrutura da Tela
- A tela deve ser maximizada ou ocupar todo o espaço disponível.
- Deve conter um **menu principal** com os seguintes módulos:
  - **Cadastro**
    - Produto
    - Cliente
  - **Pedido**
    - Solicitar Pedido
    - Pedidos

## Comportamento do Menu
- Ao clicar em **Cadastro > Produto**, deve abrir a tela `produto_form.py`.
- Ao clicar em **Cadastro > Cliente**, deve abrir a tela correspondente ao cadastro de clientes.
- Ao clicar em **Pedido > Solicitar Pedido**, deve abrir a tela de solicitação de pedidos.
- Ao clicear em **Pedido > Pedido**, deve abrir a tela de Pedidos.

## Requisitos Funcionais
- O menu deve estar sempre visível na parte superior da tela.
- Cada opção do menu deve chamar a respectiva tela ou formulário.
- A tela de Dashboard deve ser a **janela principal** da aplicação.

## Observações
- Este documento serve como guia de especificação para implementação.
- O código em Python deve ser gerado a partir desta estrutura.
