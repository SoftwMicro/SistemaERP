#fixbug

metodo def alterar_status não esta salvando ou alterando novo status na tabela order somente retornando. o mesmo fluxo para inclusão da movimentação  na tabela orderstatushistory para atender o requisito:

Registra todas as mudanças de status do pedido apos sua alteração de status.
• Data/hora, status anterior, novo status, usuário responsável 
• Observações da mudança. A tabela já existe e o domain ordem_status_history.py

fluxo:
Qualquer movimentação do status ou alteração deve registra seu historico.

  pedido.adicionar_status(novo_status, usuario, observacoes)