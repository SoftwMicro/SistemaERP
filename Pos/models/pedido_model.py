from database.db_connection import DatabaseConnection

class PedidoModel:
    @staticmethod
    def listar_todos():
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = ("SELECT o.*, c.nome as cliente_nome FROM orders_order o "
                 "JOIN orders_cliente c ON o.cliente_id = c.id")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result

    @staticmethod
    def buscar_itens_pedido(pedido_id):
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = ("SELECT * FROM orders_orderitem WHERE pedido_id = %s")
        cursor.execute(query, (pedido_id,))
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result
    
    @staticmethod
    def buscar_por_id(pedido_id):
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = ("SELECT * FROM orders_order WHERE id = %s")
        cursor.execute(query, (pedido_id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result



    @staticmethod
    def criar_pedido(data_criacao, status, valor_total, observacoes, cliente_id, idempotency_key=None):
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        query = ("INSERT INTO orders_order (data_criacao, status, valor_total, observacoes, cliente_id, idempotency_key) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (data_criacao, status, valor_total, observacoes, cliente_id, idempotency_key))
        pedido_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        db.close()
        return pedido_id

    @staticmethod
    def atualizar_status(pedido_id, novo_status):
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        query = "UPDATE orders_order SET status = %s WHERE id = %s"
        cursor.execute(query, (novo_status, pedido_id))
        conn.commit()
        cursor.close()
        db.close()

    @staticmethod
    def deletar_pedido(pedido_id):
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        # Deletar itens
        cursor.execute("DELETE FROM orders_orderitem WHERE pedido_id = %s", (pedido_id,))
        # Deletar pedido
        cursor.execute("DELETE FROM orders_order WHERE id = %s", (pedido_id,))
        conn.commit()
        cursor.close()
        db.close()
