import sqlite3

class Clientes:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("form_crud/datos.db", check_same_thread= False)

    def add_clients(self,name,age, email, phone):
        query = ''' INSERT INTO clientes(NOMBRE, EDAD, CORREO, TELEFONO)
                    VALUES(?,?,?,?)    
'''
        self.connection.execute(query, (name, age, email, phone))
        self.connection.commit()

    def get_clients(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM clientes "
        cursor.execute(query)
        clientes = cursor.fetchall()
        return clientes

    def delete_clients(self, client_id):
        query = "DELETE FROM clientes WHERE ID = ?"
        self.connection.execute(query, (client_id,))
        self.connection.commit()


    def update_clients(self,client_id,name,age,email,phone):
        query = '''UPDATE clientes SET NOMBRE = ? , EDAD = ? , CORREO = ? , TELEFONO = ? WHERE ID = ?'''
        self.connection.execute(query, (name, age, email, phone, client_id))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

