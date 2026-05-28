from database.db_connection import DatabaseConnection

class ProdutoModel:
    @staticmethod
    def listar_produtos_disponiveis():
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM orders_produto WHERE ativo = 1"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result

    @staticmethod
    def buscar_por_id(produto_id):
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM orders_produto WHERE id = %s AND ativo = 1"
        cursor.execute(query, (produto_id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result

    @staticmethod
    def atualizar_estoque(produto_id, quantidade):
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        query = "UPDATE orders_produto SET quantidade_estoque = quantidade_estoque - %s WHERE id = %s AND quantidade_estoque >= %s"
        cursor.execute(query, (quantidade, produto_id, quantidade))
        conn.commit()
        cursor.close()
        db.close()
