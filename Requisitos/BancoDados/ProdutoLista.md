# Requisitos do Módulo produto_form.py

## Arquitetura 
pasta C:\Projetos\SistemaERP\cliente

Vamos esturura aplicao em MVC

## Objetivo
Atualizar o formulário em Python com (Tkinter) produto_form.py e exibir grid abaixo do formulário com dados e requisito abaixo e também se conecta ao banco de dados **homologacao** no MySQL e exibe em um grid os atributos selecionados das tabelas relacionadas a produtos.

## Conexão com Banco de Dados
- **Servidor**: localhost  
- **Banco de Dados**: homologacao  
- **Usuário**: hmg  
- **Senha**: 010101  

## Tabelas Envolvidas
- **Produtos**
- **ProdutoDetalhes**
- **Estoques**

## Relacionamentos
- A tabela **Produtos** possui chave estrangeira para **ProdutoDetalhes** (`DetalhesId`).
- A tabela **Estoques** possui chave estrangeira para **Produtos** (`ProdutoId`).

## Atributos a Listar
- `Produtos.Id`
- `Produtos.Nome`
- `ProdutoDetalhes.Descricao`
- `ProdutoDetalhes.Ativo`
- `Estoques.QuantidadeAtual`

## Estrutura Esperada
- Criar consulta SQL que faça o relacionamento entre as tabelas **Produtos**, **ProdutoDetalhes** e **Estoques**.
- Exibir os resultados em um **grid** dentro da tela `produto_form.py`.
- O grid deve conter apenas os atributos listados acima.

## Observações
- O formulário deve ser capaz de executar a consulta e atualizar o grid com os dados do banco.
- Este documento serve como guia de especificação para implementação do código em Python.
