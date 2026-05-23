# Regras de Negócio - Módulo Pedidos

## Objetivo
Definir as regras de negócio críticas para o módulo **Pedidos**, separando a camada de negócio para permitir reutilização em outros projetos e futura integração com banco de dados. Inicialmente, o repositório será em memória para facilitar testes e migrações futuras.

## Arquitetura
Seguir arquitetura limpa (Domain, Application, Infrastructure):
- **Domain** → Entidades e regras de negócio puras.
- **Application** → Serviços e casos de uso (interagem com Domain e Repository).
- **Infrastructure** → Implementações concretas (ex.: repositório em memória, views DRF).
- **Interface (Views)** → Exposição via API REST.

## Princípios
- Seguir os princípios **SOLID**.
- Separação clara de responsabilidades.
- Camada de negócio independente de frameworks.
- Preparar abstrações para futura persistência em banco de dados.

---

## 5. Regras de Negócio Críticas

### 5.1 Controle de Estoque
- Atualizar estoque.
- Criar pedido.
- Listar pedidos.
- Obter pedido.
- Alterar status.
- Cancelar pedido.

**Regras específicas:**
- Ao criar um pedido, o estoque dos produtos deve ser reservado **atomicamente**.
- Se não houver estoque suficiente, o pedido deve ser rejeitado completamente (**tudo ou nada**).
- Múltiplos pedidos simultâneos **NÃO** podem reservar o mesmo estoque (evitar condição de corrida).
- Ao cancelar um pedido, o estoque deve ser devolvido.

---

### 5.2 Transições de Status
Fluxo válido de status:
- `PENDENTE → CONFIRMADO → SEPARADO → ENVIADO → ENTREGUE`
- `PENDENTE/CONFIRMADO → CANCELADO` (apenas estes status podem ser cancelados)

**Regras específicas:**
- Transições inválidas devem ser rejeitadas com erro apropriado.
- Cada mudança de status deve gerar um registro no histórico:
  - Data/hora da mudança.
  - Status anterior.
  - Novo status.
  - Usuário responsável.
  - Observações da mudança.

---

## Endpoints
- **POST** `/api/v1/orders` → Criar pedido
- **GET** `/api/v1/orders` → Listar pedidos
- **GET** `/api/v1/orders/:id` → Obter pedido
- **PATCH** `/api/v1/orders/:id/status` → Alterar status
- **DELETE** `/api/v1/orders/:id` → Cancelar pedido

---

## Boas práticas
- Views chamam apenas o service da camada Application.
- Service depende de abstrações (repository).
- Repository em memória implementa persistência mockada.
- Retorno sempre em JSON via DRF.
- Preparar interfaces para futura integração com banco de dados.