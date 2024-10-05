import mysql.connector

class Database:
    # Para facilitar em usos futuros decidi colocar em variaveis
    SERVER = "localhost"
    DATABASE = "fakeanalyzer"
    USUARIO = "root"
    SENHA = ""
    API_KEY = '5061441215:AAE5qnFUHG6vAOjThb2wjrDAoRWPSUiGP08'
    con = None

    @staticmethod
    def conectar():
        # Tenta conexao com o banco
        try:
            Database.con = mysql.connector.connect(
                database=Database.DATABASE,
                user=Database.USUARIO,
                password=Database.SENHA,
                host=Database.SERVER,
            )
        except Exception as ex:
            raise ex 
            
    @staticmethod
    def desconectar():
        try:
            if Database.con is not None:
                Database.con.close()
        except Exception as ex:
            raise ex
    
    @staticmethod
    def executarSelect(queryStmt):
        cursor = None
        try:
            Database.conectar()
            cursor = Database.con.cursor()
            cursor.execute(queryStmt)
            result = cursor.fetchall()
            return result
        except Exception as ex:
            print(f"Ocorreu um problema ao tentar executar o Select: {ex}")
            raise ex
        finally:
            # Desconecta tudo para nao ter vazamento de memoria
            if cursor is not None:
                cursor.close()
            Database.desconectar()
    
    @staticmethod
    def executarQuery(queryStmt):
        cursor = None
        try:
            Database.conectar()
            cursor = Database.con.cursor()
            cursor.execute(queryStmt)
            Database.con.commit()
        except Exception as ex:
            print(f"Ocorreu um problema ao tentar executar a Query: {ex}")
            raise ex
        finally:
            # Deconecta tudo
            if cursor is not None:
                cursor.close()
            Database.desconectar()

