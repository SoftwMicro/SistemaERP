# Documentação de Requisito: Histórico de Status de Pedido

## 1. Problema Identificado
Atualmente, o método `alterar_status` em `order_service.py` apresenta:
* **Persistência Incorreta:** Possível criação de novos registros em vez de atualização do existente.
* **Ausência de Log:** Falta de registro histórico das transições de estado do pedido.

## 2. Objetivo
Modificar o fluxo de atualização para garantir que o pedido seja identificado pelo ID, atualizado, e que um registro de auditoria seja gerado na entidade `OrderStatusHistory`.

---

## 3. Estrutura da Entidade: `OrderStatusHistory`

A classe de histórico deve ser instanciada com os seguintes atributos:

| Atributo | Descrição |
| :--- | :--- |
| `data_hora` | Timestamp do momento da alteração. |
| `status_anterior` | O estado em que o pedido se encontrava antes da mudança. |
| `novo_status` | O novo estado aplicado ao pedido. |
| `usuario` | Identificação de quem realizou a alteração. |
| `idempotency_key` | **(Novo)** Chave para garantir a rastreabilidade e unicidade da operação. |
| `observacoes` | Campo opcional para detalhes adicionais (Padrão: `None`). |

---

## 4. Fluxo de Execução (To-Be)



1. **Recuperação:** Buscar o pedido na base de dados utilizando o `ID`.
2. **Captura de Estado:** Armazenar o status atual do pedido como `status_anterior`.
3. **Atualização do Pedido:** * Alterar o atributo `status` para o `novo_status`.
   * Realizar o **Update** do pedido no banco de dados.
4. **Registro de Histórico:** Instanciar e persistir `OrderStatusHistory` com os atributos definidos acima, incluindo a `idempotency_key` recebida no processo.
5. **Confirmação:** Garantir que ambas as operações (Update e Log) sejam atômicas (dentro de uma transação).

---

> **Atenção:** A `idempotency_key` é obrigatória para evitar que o mesmo evento de alteração de status seja processado e registrado mais de uma vez no histórico.