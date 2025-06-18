import tkinter as tk  # Importa la librería de interfaz gráfica Tkinter
from tkinter import messagebox, ttk  # Importa cuadros de mensajes y widgets avanzados
from basededatos import subir_libro, buscar_libros, actualizar_libro  # Importa funciones definidas en otro archivo

CATEGORIAS_VALIDAS = ["Ciencia", "Literatura", "Ingeniería"]  # Lista de categorías permitidas para validar

# Valida que los campos del formulario estén completos y que la categoría sea válida
def validar_campos(titulo, autor, categoria):
    if not titulo or not autor or not categoria:  # Si falta algún campo
        messagebox.showerror("Error", "Todos los campos son obligatorios.")  # Muestra error
        return False
    if categoria not in CATEGORIAS_VALIDAS:  # Si la categoría no es válida
        messagebox.showerror("Error", f"Categoría inválida. Debe ser una de: {', '.join(CATEGORIAS_VALIDAS)}")  # Mensaje de error
        return False
    return True  # Devuelve True si todo es válido

# Función para registrar un nuevo libro
def registrar_libro():
    titulo = entry_titulo.get()  # Obtiene el título del Entry
    autor = entry_autor.get()  # Obtiene el autor
    categoria = combo_categoria.get()  # Obtiene la categoría del combobox
    disponible = True  # El libro está disponible al registrarse

    if validar_campos(titulo, autor, categoria):  # Valida campos antes de guardar
        libro = {
            "titulo": titulo,
            "autor": autor,
            "categoria": categoria,
            "disponible": disponible
        }
        if subir_libro(libro):  # Llama a función que guarda el libro en la base de datos
            messagebox.showinfo("Éxito", "Libro registrado correctamente.")  # Éxito
        else:
            messagebox.showerror("Error", "No se pudo registrar el libro.")  # Fallo al guardar

# Función para buscar libros por título o autor
def buscar():
    criterio = combo_busqueda.get().lower()  # Obtiene el criterio seleccionado (titulo o autor)
    valor = entry_busqueda.get()  # Toma el valor a buscar

    resultados = buscar_libros(criterio, valor)  # Llama la función para obtener resultados
    lista_resultados.delete(0, tk.END)  # Limpia la lista antes de mostrar resultados

    for key, libro in resultados.items():  # Recorre los libros encontrados
        estado = "Disponible" if libro["disponible"] else "Prestado"  # Determina el estado
        lista_resultados.insert(tk.END, f"{key} | {libro['titulo']} - {libro['autor']} [{estado}]")  # Muestra en la lista

# Cambia el estado de un libro seleccionado (prestado o devuelto)
def marcar_estado(prestado=True):
    seleccion = lista_resultados.get(tk.ACTIVE)  # Obtiene el libro seleccionado
    if not seleccion:
        messagebox.showerror("Error", "Seleccione un libro de la lista.")  # Muestra error si no hay selección
        return
    key = seleccion.split(" | ")[0]  # Extrae el ID del libro desde el texto
    if actualizar_libro(key, {"disponible": not prestado}):  # Actualiza el estado en la base de datos
        messagebox.showinfo("Éxito", "Estado actualizado.")  # Mensaje de éxito
        buscar()  # Actualiza la lista automáticamente
    else:
        messagebox.showerror("Error", "No se pudo actualizar el estado.")  # Mensaje de error

# ---------- INTERFAZ GRÁFICA ----------

root = tk.Tk()  # Crea la ventana principal
root.title("Inventario de Biblioteca")  # Título de la ventana
root.geometry("600x500")  # Tamaño fijo de la ventana

tk.Label(root, text="Título").pack()  # Etiqueta para el título
entry_titulo = tk.Entry(root)  # Campo de entrada para el título
entry_titulo.pack()  # Agrega al diseño

tk.Label(root, text="Autor").pack()  # Etiqueta para autor
entry_autor = tk.Entry(root)  # Campo de entrada para autor
entry_autor.pack()  # Agrega al diseño

tk.Label(root, text="Categoría").pack()  # Etiqueta para categoría
combo_categoria = ttk.Combobox(root, values=CATEGORIAS_VALIDAS)  # Combobox con categorías válidas
combo_categoria.pack()  # Agrega al diseño

tk.Button(root, text="Registrar Libro", command=registrar_libro).pack(pady=10)  # Botón que llama a registrar_libro

tk.Label(root, text="Buscar por título o autor").pack()  # Etiqueta para búsqueda
combo_busqueda = ttk.Combobox(root, values=["titulo", "autor"])  # Combobox para seleccionar el tipo de búsqueda
combo_busqueda.set("titulo")  # Selección por defecto
combo_busqueda.pack()  # Agrega al diseño

entry_busqueda = tk.Entry(root)  # Campo de entrada para el texto a buscar
entry_busqueda.pack()  # Agrega al diseño

tk.Button(root, text="Buscar", command=buscar).pack(pady=5)  # Botón que ejecuta la búsqueda

lista_resultados = tk.Listbox(root, width=80, height=10)  # Lista para mostrar resultados de libros
lista_resultados.pack(pady=10)  # Agrega con margen vertical

tk.Button(root, text="Marcar como Prestado", command=lambda: marcar_estado(prestado=True)).pack()  # Botón para marcar libro como prestado
tk.Button(root, text="Marcar como Devuelto", command=lambda: marcar_estado(prestado=False)).pack()  # Botón para marcar como devuelto

root.mainloop()  # Inicia la interfaz gráfica (bucle principal)
