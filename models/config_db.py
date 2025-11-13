import mysql.connector
from mysql.connector import Error

class Database:
    
    CONFIG = {
        'host': 'localhost',
        'user': 'root',             
        'password': 'Zinderellasnuff_344',              
        'database': 'gestion_clientes_jp',
        'charset': 'utf8mb4'
    }
    
    _connection = None
    
    @classmethod
    def conectar(cls):
        try:
            if cls._connection is None or not cls._connection.is_connected():
                cls._connection = mysql.connector.connect(**cls.CONFIG)
                print("✓ Conectado a MySQL")
            return cls._connection
        except Error as e:
            print(f"✗ Error de conexión: {e}")
            raise
    
    @classmethod
    def cerrar(cls):
        if cls._connection and cls._connection.is_connected():
            cls._connection.close()
            print("✓ Conexión cerrada")

if __name__ == "__main__":
    try:
        Database.conectar()
        print("✓ Conectado a MySQL")
        Database.cerrar()
    except:
        print("✗ Error de conexión")