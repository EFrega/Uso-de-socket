import socket # Importa el módulo para trabajar con sockets (conexiones TCP/IP)
import sqlite3 # Importa el módulo para trabajar con bases de datos SQLite
from datetime import datetime # Importa para obtener la fecha y hora actuales

# Configuración de la base de datos
def inicializarDB():
    conn = sqlite3.connect('mensajes.db') # Conecta a la base de datos 'mensajes.db' y si no existe crea la base de datos 'mensajes.db'
    cursor = conn.cursor() # Crea un cursor para ejecutar comandos SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT NOT NULL,
            fecha_envio TEXT NOT NULL,
            ip_cliente TEXT NOT NULL
        )
    ''')
    conn.commit() # Guarda los cambios en la base de datos
    conn.close() # Cierra la conexión con la base de datos

def guardar_mensaje(contenido, ip_cliente):
    conn = sqlite3.connect('mensajes.db')
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)", (contenido, fecha_actual, ip_cliente))
    conn.commit()
    conn.close()

def inicializar_socket():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        servidor_socket.bind(("localhost", 5000))
        servidor_socket.listen(5)
        print("Servidor iniciado en el puerto 5000")
        return servidor_socket
    except OSError as e:
        print(f"Error al iniciar el servidor: {e}")
        exit()

def manejar_conexion(servidor_socket):
    while True:
        cliente_socket, direccion = servidor_socket.accept()
        print(f"Conexión establecida con {direccion}")
        try:
            while True:
                mensaje = cliente_socket.recv(1024).decode()
                if not mensaje:
                    break
                timestamp = guardar_mensaje(mensaje, direccion[0]).strftime("%Y-%m-%d %H:%M:%S")
                respuesta = f"Mensaje recibido en {timestamp}: {mensaje}"
                cliente_socket.sendall(respuesta.encode())
        except Exception as e:
            print(f"Error al manejar la conexión con {direccion}: {e}")
        finally:
            cliente_socket.close()
            print(f"Conexión cerrada con {direccion}")

if __name__ == "__main__":
    inicializarDB()
    servidor_socket = inicializar_socket()
    manejar_conexion(servidor_socket)
    servidor_socket.close()
    

