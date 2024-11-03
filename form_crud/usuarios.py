# db_handler.py
import sqlite3

def check_user(email, password):
    try:
        connection = sqlite3.connect("form_crud/datos.db")
        cursor = connection.cursor()
        query = "SELECT * FROM usuarios WHERE email = ? AND password = ?"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        connection.close()
        return user is not None  # Devuelve True si el usuario existe, False en caso contrario
    except sqlite3.Error as e:
        print("Error al conectar con la base de datos:", e)
        return False
