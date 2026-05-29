# Requisitos do Sistema - Financeiro (Aplicação Desktop em Python)

## 1. Objetivo
Desenvolver um módulo **Financeiro** como aplicação desktop em Python, integrado ao banco de dados `pedidos`.  
A aplicação deve seguir arquitetura **MVC** organizada na pasta `Financeiro`, com camadas separadas para **Model**, **View** e **Controller**.


## Conexão com Banco de Dados
self.connection = mysql.connector.connect(
host='localhost',
database='pedidos',
user='admin',
password='010101',
port=3306
)


## 3. Fluxo de Operação

### 3.1 Tela de Login
- Usuário informa **login** e **senha**.
- Validar credenciais na tabela `orders_usuario`.
- Verificar se usuário está ativo (`ativo = TRUE`).
- Se válido, acessar o sistema financeiro.

### 3.2 Registro de Usuário
- Na tela de login aparecer opção registra novo usuário caso não exista.
- Tela para cadastrar novos usuários.
- Campos obrigatórios:
  - Nome
  - Login (único)
  - Senha (armazenada como hash seguro)
  - Perfil (Caixa, Gerente, Admin)
  - Ativo (boolean)
- Inserir dados na tabela `orders_usuario`.

### 3.3 Operações de Caixa
- **Abertura de Caixa**:
  - Inserir registro em `orders_caixa` com:
    - `usuario_id`
    - `data_abertura`
    - `saldo_inicial`
    - `status = ABERTO`
- **Fechamento de Caixa**:
  - Atualizar registro em `orders_caixa` com:
    - `data_fechamento`
    - `saldo_final`
    - `status = FECHADO`

### 3.4 Pagamentos
- Registrar pagamento vinculado a um pedido.
- Inserir em `orders_pagamento`:
  - `order_id`
  - `forma_pagamento` (Dinheiro, Cartão, Pix, etc.)
  - `valor_pago`
  - `data_pagamento`
  - `status_pagamento` (Aprovado, Pendente, Cancelado)
- Validar se pedido existe em `orders_order`.

### 3.5 Comprovantes
- Emitir comprovante vinculado ao pedido.
- Inserir em `orders_receipt`:
  - `order_id`
  - `numero_comprovante`
  - `tipo` (Fiscal, Não Fiscal)
  - `data_emissao`

---

## 4. Requisitos Funcionais

- **Login**:
  - Autenticação segura com hash de senha.
  - Bloqueio de acesso para usuários inativos.

- **Cadastro de Usuário**:
  - Interface para inserir e editar usuários.
  - Validação de login único.

- **Caixa**:
  - Abertura com saldo(formatação moeda brazil) inicial obrigatório.
  - Fechamento com saldo(formatação moeda brazil) final obrigatório.
  - Status controlado (ABERTO/FECHADO).

- **Pagamentos**:
  - Seleção de pedido existente.
  - Registro de forma de pagamento e valor.
  - Atualização de status do pagamento.

- **Comprovantes**:
  - Emissão vinculada ao pedido.
  - Registro de número e tipo de comprovante.

- **Interface Gráfica (View)**:
  - Grids para listar:
    - Usuários
    - Caixas abertos/fechados
    - Pagamentos realizados
    - Comprovantes emitidos
  - Botões com feedback visual (loading, sucesso, erro).

---

## 5. Padrão Arquitetural
Utilizar boas práticas Design Patterns e clean code.

- **Model**:
  - Classes representando tabelas (`orders_usuario`, `orders_caixa`, `orders_pagamento`, `orders_receipt`).
  - Métodos de persistência (CRUD).
- **View**:
  - Interface gráfica em Tkinter/PyQt.
  - Telas: Login, Cadastro de Usuário, Caixa, Pagamentos, Comprovantes.
- **Controller**:
  - Lógica de negócio.
  - Validação de dados.
  - Integração entre View e Model.


---

## 6. Estrutura do Banco de Dados

### orders_usuario
- Usuários do sistema financeiro.
- Campos: id, nome, login, senha_hash, perfil, ativo.

### orders_caixa
- Controle de abertura e fechamento de caixa.
- Campos: id, usuario_id, data_abertura, data_fechamento, saldo_inicial, saldo_final, status.

### orders_pagamento
- Registro de pagamentos vinculados a pedidos.
- Campos: id, order_id, forma_pagamento, valor_pago, data_pagamento, status_pagamento.

### orders_receipt
- Emissão de comprovantes vinculados a pedidos.
- Campos: id, order_id, numero_comprovante, tipo, data_emissao.

---

## 7. Observações
- Todas as operações devem ser **transacionais** (rollback em caso de erro).
- Senhas devem ser armazenadas com **hash seguro** (ex.: bcrypt).
- Botões devem ser desabilitados durante execução de operações.
- Mensagens de feedback claras:
  - Sucesso (verde).
  - Erro (vermelho).

## 8. Estrutura banco de dados e relacionamento.

CREATE TABLE `orders_pagamento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NOT NULL,
  `forma_pagamento` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `valor_pago` decimal(12,2) NOT NULL,
  `data_pagamento` datetime(6) NOT NULL,
  `status_pagamento` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_pagamento_order_id_fk` (`order_id`),
  CONSTRAINT `orders_pagamento_order_id_fk` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `orders_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `login` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL UNIQUE,
  `senha_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `perfil` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ativo` boolean NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `orders_caixa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `data_abertura` datetime(6) NOT NULL,
  `data_fechamento` datetime(6) DEFAULT NULL,
  `saldo_inicial` decimal(12,2) NOT NULL,
  `saldo_final` decimal(12,2) DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_caixa_usuario_id_fk` (`usuario_id`),
  CONSTRAINT `orders_caixa_usuario_id_fk` FOREIGN KEY (`usuario_id`) REFERENCES `orders_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `orders_receipt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NOT NULL,
  `numero_comprovante` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `data_emissao` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_receipt_order_id_fk` (`order_id`),
  CONSTRAINT `orders_receipt_order_id_fk` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

