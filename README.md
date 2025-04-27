# Propuesta Formativa Obligatoria

## Trabajo Práctico: Implementación de un Chat Básico Cliente-Servidor con Sockets y Base de Datos

### Objetivo
Aprender a configurar un servidor de sockets en Python que reciba mensajes de clientes, los almacene en una base de datos y envíe confirmaciones, aplicando buenas prácticas de modularización y manejo de errores.  
Utilizar los comentarios para explicar las configuraciones en el servidor.

---

### Servidor
- Crear un socket que escuche en `localhost:5000`.
- Utilizar funciones separadas para:
  - Inicializar el socket.
  - Aceptar conexiones y recibir mensajes.
  - Guardar cada mensaje en una base de datos SQLite con los campos:
    - `id`
    - `contenido`
    - `fecha_envio`
    - `ip_cliente`
  - Manejar errores como:
    - Puerto ocupado.
    - Base de datos no accesible.
  - Responder al cliente con:  
    `"Mensaje recibido: <timestamp>"`.

---

### Cliente
- Debe tener la capacidad de conectarse al servidor y enviar múltiples mensajes hasta que el usuario escriba `éxito`.
- Mostrar la respuesta del servidor para cada mensaje.

---

### Recomendaciones
- Utilizar el módulo `sqlite3` para manejar la base de datos.
- Comentar cada sección clave, por ejemplo:
  ```python
  # Configuración del socket TCP/IP
