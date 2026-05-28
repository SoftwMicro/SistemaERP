from database.db_connection import DatabaseConnection

class ClienteModel:
    @staticmethod
    def buscar_por_cpf_cnpj(cpf_cnpj):
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM orders_cliente WHERE cpf_cnpj = %s AND ativo = 1"
        cursor.execute(query, (cpf_cnpj,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result

    @staticmethod
    def buscar_por_id(cliente_id):
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM orders_cliente WHERE id = %s AND ativo = 1"
        cursor.execute(query, (cliente_id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result

    @staticmethod
    def pesquisar_clientes(filtro):
        id_busca = filtro if str(filtro).isdigit() else None
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM orders_cliente WHERE id = %s OR ((cpf_cnpj LIKE %s OR nome LIKE %s) AND ativo = 1)"
        filtro_texto = f"%{filtro}%"
        cursor.execute(query, (id_busca, filtro_texto, filtro_texto))
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result
