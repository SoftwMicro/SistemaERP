# Arquitetura do Sistema ERP - Pedidos API

## Padrões Arquiteturais Adotados
- **Camadas (Domain-Driven Design):**
  - **Domain:** Entidades e regras de negócio puras
  - **Application:** Serviços de aplicação, orquestração de casos de uso
  - **Infrastructure:** Integração com frameworks, views, repositórios, serialização
- **RESTful API:** Endpoints organizados por recurso seguindo boas práticas REST
- **Repository Pattern:** Abstração de acesso a dados
- **Service Layer:** Lógica de aplicação centralizada

## Fluxo de Dados
1. **Request** chega via endpoint (View/Infrastructure)
2. View chama serviço de aplicação (Application)
3. Serviço de aplicação orquestra entidades e repositórios (Domain/Infrastructure)
4. Dados são persistidos/recuperados via repositórios
5. Resposta é serializada e retornada ao cliente

```
[Client] → [View/Infra] → [Service/App] → [Domain] → [Repository/Infra] → [DB/Redis]
```

## Decisões Técnicas e Trade-offs
- **Django REST Framework:** Facilidade para criar APIs robustas, autenticação, validação e serialização
- **drf-yasg (Swagger):** Documentação automática e interativa
- **Separação de camadas:** Facilita testes, manutenção e evolução, mas aumenta a quantidade de arquivos
- **Redis:** Usado para cache e filas, melhora performance, mas adiciona dependência externa
- **Docker:** Facilita setup local e deploy, mas pode ser complexo para iniciantes
- **Pytest:** Testes mais simples e legíveis, integração fácil com CI

## Observações
- O projeto prioriza clareza, testabilidade e extensibilidade
- Decisões podem ser revistas conforme o crescimento do sistema
