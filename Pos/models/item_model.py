from database.db_connection import DatabaseConnection

class ItemModel:
    @staticmethod
    def inserir_itens(pedido_id, itens):
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        query = ("INSERT INTO orders_orderitem (quantidade, preco_unitario, subtotal, pedido_id, produto_id) "
                 "VALUES (%s, %s, %s, %s, %s)")
        for item in itens:
            cursor.execute(query, (
                item['quantidade'],
                item['preco_unitario'],
                item['subtotal'],
                pedido_id,
                item['produto_id']
            ))
        conn.commit()
        cursor.close()
        db.close()
