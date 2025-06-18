import json  # Importa el módulo para manejar archivos y datos en formato JSON
import requests  # Importa la librería que permite hacer solicitudes HTTP (GET, POST, PATCH)

# URL base de la base de datos de Firebase (Realtime Database)
FIREBASE_URL = "https://parcial2-c7d8a-default-rtdb.firebaseio.com/"

# Ruta local al archivo JSON que contiene la clave de autenticación (en este caso, no se está usando para autenticar directamente)
RUTA_CREDENCIALES = r"C:\Users\ESTUDIANTES\Documents\PROGRAMACIÓN DE COMPUTADORES\ACTIVIDAD INICIAL\parcial2\claveparcial2.json"

# Carga las credenciales desde un archivo JSON local (aunque no se usan en esta versión con requests)
def cargar_credenciales():
    with open(RUTA_CREDENCIALES, 'r') as f:  # Abre el archivo JSON en modo lectura
        return json.load(f)  # Devuelve los datos cargados como diccionario

# Sube un nuevo libro a Firebase
def subir_libro(libro):
    response = requests.post(FIREBASE_URL + "libros.json", json=libro)  # Envía una solicitud POST para crear un nuevo libro
    return response.ok  # Devuelve True si la solicitud fue exitosa

# Obtiene todos los libros registrados en Firebase
def obtener_libros():
    response = requests.get(FIREBASE_URL + "libros.json")  # Solicita todos los libros con una solicitud GET
    if response.ok and response.json():  # Si la respuesta fue exitosa y contiene datos
        return response.json()  # Devuelve los datos como diccionario
    return {}  # Si no hay libros o hay error, retorna diccionario vacío

# Actualiza los datos de un libro específico
def actualizar_libro(key, data):
    response = requests.patch(FIREBASE_URL + f"libros/{key}.json", json=data)  # Envía una solicitud PATCH para modificar campos del libro
    return response.ok  # Devuelve True si la actualización fue exitosa

# Busca libros por un campo (filtro) y valor (título o autor)
def buscar_libros(filtro, valor):
    libros = obtener_libros()  # Obtiene todos los libros de Firebase
    resultado = {}  # Inicializa el diccionario de resultados
    for key, libro in libros.items():  # Recorre todos los libros
        if valor.lower() in libro.get(filtro, "").lower():  # Si el valor buscado está dentro del campo solicitado (sin distinguir mayúsculas)
            resultado[key] = libro  # Agrega el libro al resultado
    return resultado  # Devuelve los libros que coinciden con la búsqueda
