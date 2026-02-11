# Prompt para GitHub Copilot (GPT-4.1)

Quero criar um novo módulo chamado **Products** dentro do projeto Django seguindo a arquitetura limpa e os princípios SOLID já utilizados nos módulos anteriores (Orders e Clientes).

## Estrutura de pastas e arquivos
Dentro do app `orders/` criar:

- `domain/product.py` → Entidade Produto (SKU, nome, descrição, preço, quantidade em estoque, status ativo/inativo).
- `application/product_service.py` → Casos de uso (criar produto, listar produtos, atualizar estoque).
- `infrastructure/repository_product.py` → Repositório em memória para Produto.
- `infrastructure/views_product.py` → Views DRF para expor endpoints.
- Atualizar `orders/urls.py` → incluir rotas de produtos.

## Requisitos funcionais
- **POST** `/api/v1/products` → Criar produto
- **GET** `/api/v1/products` → Listar produtos
- **PATCH** `/api/v1/products/:id/stock` → Atualizar estoque

## Regras
- Seguir arquitetura limpa (Domain, Application, Infrastructure).
- Cada camada deve ter responsabilidade única.
- Views chamam apenas o service da camada Application.
- Service depende de abstrações (repository).
- Repository em memória implementa persistência mockada.
- Retorno sempre em JSON via DRF.

## Objetivo
Gerar automaticamente os arquivos e código Python necessários para implementar o módulo **Products** seguindo o padrão já estabelecido.