from database.db_connection import DatabaseConnection

class StatusHistoryModel:
    @staticmethod
    def inserir_status(pedido_id, status_anterior, novo_status, usuario, observacoes=None, idempotency_key=None):
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        query = ("INSERT INTO orders_orderstatushistory (data_hora, status_anterior, novo_status, usuario, observacoes, pedido_id, idempotency_key) "
                 "VALUES (NOW(), %s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (status_anterior, novo_status, usuario, observacoes, pedido_id, idempotency_key))
        conn.commit()
        cursor.close()
        db.close()
