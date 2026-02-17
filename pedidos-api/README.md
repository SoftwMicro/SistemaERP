# Sistema ERP - Pedidos API

## Descrição do Projeto
API para gestão de pedidos, clientes e produtos de um sistema ERP, com endpoints RESTful, documentação interativa (Swagger) e integração com Redis e MySQL.

## Tecnologias Utilizadas
- Python 3.14
- Django 6
- Django REST Framework
- drf-yasg (Swagger)
- MySQL
- Redis
- Docker / Docker Compose
- Pytest

## Pré-requisitos
- Python 3.10+
- Docker e Docker Compose
- MySQL
- Redis
- (Opcional) Ambiente virtual Python

## Como rodar localmente (passo a passo)
1. Clone o repositório:
   ```sh
   git clone <repo-url>
   cd pedidos-api
   ```
2. Crie e ative um ambiente virtual:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure o banco de dados e Redis (ou use Docker Compose):
   ```sh
   docker-compose up -d
   ```
5. Execute as migrações:
   ```sh
   python manage.py migrate
   ```
6. Inicie o servidor:
   ```sh
   python manage.py runserver
   ```
7. Acesse a documentação interativa:
   - [http://localhost:8000/docs/](http://localhost:8000/docs/)
   - [http://localhost:8000/api-docs/](http://localhost:8000/api-docs/)

## Como rodar os testes
```sh
pytest
```

## Estrutura de Pastas
```
pedidos-api/
├── core/                # Configurações principais do projeto Django
├── orders/              # App principal: domínio, aplicação, infraestrutura
│   ├── application/     # Serviços de aplicação
│   ├── domain/          # Entidades e lógica de domínio
│   ├── infrastructure/  # Views, repositórios, integrações
│   └── migrations/      # Migrações do banco de dados
├── tests/               # Testes unitários e de integração
├── mysql-init/          # Scripts de inicialização do MySQL
├── Dockerfile           # Dockerfile do projeto
├── docker-compose.yml   # Orquestração de containers
├── manage.py            # Entrypoint Django
└── README.md            # Este arquivo
```

## Decisões Arquiteturais Importantes
- Separação em camadas: domínio, aplicação, infraestrutura
- Uso de Django REST Framework para APIs
- Documentação automática com Swagger (drf-yasg)
- Integração com Redis para cache e filas
- Banco de dados relacional (MySQL)
- Testes automatizados com Pytest
- Suporte a Docker para ambiente local

Para detalhes arquiteturais, veja [ARCHITECTURE.md](ARCHITECTURE.md).
