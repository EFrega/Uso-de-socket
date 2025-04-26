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
    conn = sqlite3.connect('mensajes.db') # Conecta con la base de datos
    cursor = conn.cursor() # Crea un cursor para ejecutar comandos SQL
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Obtiene el timestamp actual como string
    cursor.execute("INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)", (contenido, fecha_actual, ip_cliente)) # Inserta un nuevo registro en la tabla 'mensajes' usando parámetros seguros
    conn.commit() # Guarda los cambios
    conn.close() # Cierra la conexión con la base de datos
    return fecha_actual # Retorna el timestamp para confirmar al cliente el momento en que se guardó el mensaje

def inicializar_socket():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea un socket TCP/IP
    try:
        servidor_socket.bind(("localhost", 5000)) # Asocia el socket a localhost en el puerto 5000
        servidor_socket.listen(5) # Permite que el socket escuche hasta 5 conexiones simultáneas en espera
        print("Servidor iniciado en el puerto 5000") # Mensaje de confirmación en consola
        return servidor_socket # Devuelve el socket inicializado y preparado para aceptar conexiones
    except OSError as e:
        print(f"Error al iniciar el servidor: {e}") # Imprime el error si falla la creación del socket
        exit() # Termina el programa

def manejar_conexion(servidor_socket):
    while True: # Bucle infinito para manejar múltiples conexiones de clientes
        cliente_socket, direccion = servidor_socket.accept() # Acepta una nueva conexión de cliente
        print(f"Conexión establecida con {direccion}") # Imprime la dirección IP y puerto del cliente conectado
        try:
            while True: # Bucle para recibir múltiples mensajes de un mismo cliente
                mensaje = cliente_socket.recv(1024).decode() # Recibe hasta 1024 bytes del cliente y los decodifica
                if not mensaje: # Si no recibe datos (cliente desconectado), rompe el bucle
                    break
                timestamp = guardar_mensaje(mensaje, direccion[0]).strftime("%Y-%m-%d %H:%M:%S") # Llama a guardar el mensaje y obtiene el timestamp
                respuesta = f"Mensaje recibido en {timestamp}: {mensaje}" # Crea el mensaje de respuesta con el timestamp
                cliente_socket.sendall(respuesta.encode()) # Envía la respuesta al cliente
        except Exception as e: # Si ocurre algún error durante el manejo de la conexión
            print(f"Error al manejar la conexión con {direccion}: {e}") # Imprime el error
        finally:
            cliente_socket.close() # Cierra la conexión del cliente
            print(f"Conexión cerrada con {direccion}") # Informa que la conexión con el cliente se ha cerrado

if __name__ == "__main__":
    inicializarDB() # Llama a la función para inicializar la base de datos (crear la tabla 'mensajes')
    servidor_socket = inicializar_socket() # Llama a la función para inicializar el socket del servidor
    manejar_conexion(servidor_socket) # Llama a la función para manejar las conexiones de los clientes
    servidor_socket.close() # Cierra el socket del servidor (aunque en este caso nunca se alcanza por el bucle infinito)
    

