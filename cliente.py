import socket # Importa el módulo para trabajar con sockets (conexiones TCP/IP)

def cliente_chat():
    # Configuración del socket del cliente
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea un socket TCP/IP
    try:
        cliente_socket.connect(("localhost", 5000)) # Conecta al servidor en localhost en el puerto 5000
        print("Conectado al servidor") # Mensaje de confirmación en consola
        while True: # Bucle infinito para enviar y recibir mensajes del servidor
            mensaje = input("Ingrese un mensaje: ") # Solicita al usuario un mensaje para enviar al servidor
            if mensaje.lower() == "éxito":
                break # Si el usuario escribe "éxito", rompe el bucle y termina el chat
            cliente_socket.sendall(mensaje.encode()) # Envia el mensaje al servidor
            respuesta = cliente_socket.recv(1024).decode() # Recibe hasta 1024 bytes del servidor y los decodifica
            print(f"Respuesta del servidor: {respuesta}") # Imprime la respuesta del servidor en consola
    except OSError as e:
        print(f"Error al conectar al servidor: {e}") # Imprime el error si falla la conexión con el servidor
    finally:
        cliente_socket.close() # Cierra la conexión con el servidor tras finalizar el envío de mensajes
        print("Conexión con el servidor cerrada") # Mensaje de confirmación en consola

if __name__ == "__main__": # Si el archivo se ejecuta directamente (no importado como módulo)
    cliente_chat()  # Llama a la función para iniciar el chat
    print("Gracias por usar el chat!")
