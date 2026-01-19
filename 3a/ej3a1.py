"""
Enunciado:
En este ejercicio aprenderás a utilizar la biblioteca sqlite3 de Python para trabajar
con bases de datos SQLite. SQLite es una base de datos liviana que no requiere un servidor
y almacena la base de datos completa en un solo archivo.

Tareas:
1. Conectar a una base de datos SQLite
2. Crear tablas usando SQL
3. Insertar, actualizar, consultar y eliminar datos
4. Manejar transacciones y errores

Este ejercicio se enfoca en las operaciones básicas de SQL desde Python sin utilizar un ORM.
"""

import sqlite3

# Ruta de la base de datos (en memoria para este ejemplo)
# Para una base de datos en archivo, usar: 'biblioteca.db'
DB_PATH = ":memory:"


def _fix_text(text):
    if isinstance(text, str):
        try:
            return text.encode("latin1").decode("utf-8")
        except UnicodeError:
            return text
    return text


def crear_conexion():
    """
    Crea y devuelve una conexión a la base de datos SQLite
    """
    return sqlite3.connect(DB_PATH)


def crear_tablas(conexion):
    """
    Crea las tablas necesarias para la biblioteca:
    - autores: id (entero, clave primaria), nombre (texto, no nulo)
    - libros: id (entero, clave primaria), titulo (texto, no nulo),
              anio (entero), autor_id (entero, clave foránea a autores.id)
    """
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS autores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            anio INTEGER,
            autor_id INTEGER,
            FOREIGN KEY (autor_id) REFERENCES autores(id)
        );
    """)

    conexion.commit()


def insertar_autores(conexion, autores):
    """
    Inserta varios autores en la tabla 'autores'
    Parámetro autores: Lista de tuplas (nombre,)
    """
    cursor = conexion.cursor()
    cursor.executemany("INSERT INTO autores (nombre) VALUES (?)", autores)
    conexion.commit()


def insertar_libros(conexion, libros):
    """
    Inserta varios libros en la tabla 'libros'
    Parámetro libros: Lista de tuplas (titulo, anio, autor_id)
    """
    cursor = conexion.cursor()
    cursor.executemany(
        "INSERT INTO libros (titulo, anio, autor_id) VALUES (?, ?, ?)", libros
    )
    conexion.commit()


def consultar_libros(conexion):
    """
    Consulta todos los libros y muestra título, año y nombre del autor
    """
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT libros.titulo, libros.anio, autores.nombre
        FROM libros
        JOIN autores ON libros.autor_id = autores.id
        ORDER BY libros.id;
    """)

    for titulo, anio, autor in cursor.fetchall():
        print(f"{_fix_text(titulo)} ({anio}) - {_fix_text(autor)}")


def buscar_libros_por_autor(conexion, nombre_autor):
    """
    Busca libros por el nombre del autor
    """
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT libros.titulo, libros.anio, autores.nombre
        FROM libros
        JOIN autores ON libros.autor_id = autores.id;
    """)

    resultados = []
    nombre_autor_fix = _fix_text(nombre_autor)

    for titulo, anio, autor in cursor.fetchall():
        if _fix_text(autor) == nombre_autor_fix:
            resultados.append((_fix_text(titulo), anio))

    return resultados


def actualizar_libro(conexion, id_libro, nuevo_titulo=None, nuevo_anio=None):
    """
    Actualiza la información de un libro existente
    """
    cursor = conexion.cursor()
    campos = []
    valores = []

    if nuevo_titulo is not None:
        campos.append("titulo = ?")
        valores.append(nuevo_titulo)

    if nuevo_anio is not None:
        campos.append("anio = ?")
        valores.append(nuevo_anio)

    if not campos:
        return

    valores.append(id_libro)

    sql = f"UPDATE libros SET {', '.join(campos)} WHERE id = ?"
    cursor.execute(sql, valores)
    conexion.commit()


def eliminar_libro(conexion, id_libro):
    """
    Elimina un libro por su ID
    """
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
    conexion.commit()


def ejemplo_transaccion(conexion):
    """
    Demuestra el uso de transacciones para operaciones agrupadas
    """
    try:
        conexion.execute("BEGIN TRANSACTION")

        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO libros (titulo, anio, autor_id) VALUES (?, ?, ?)",
            ("Libro temporal", 2024, 1),
        )

        conexion.commit()
    except sqlite3.Error:
        conexion.rollback()


if __name__ == "__main__":
    try:
        # Crear una conexión
        conexion = crear_conexion()

        print("Creando tablas...")
        crear_tablas(conexion)

        # Insertar autores
        autores = [
            ("Gabriel García Márquez",),
            ("Isabel Allende",),
            ("Jorge Luis Borges",),
        ]
        insertar_autores(conexion, autores)
        print("Autores insertados correctamente")

        # Insertar libros
        libros = [
            ("Cien años de soledad", 1967, 1),
            ("El amor en los tiempos del cólera", 1985, 1),
            ("La casa de los espíritus", 1982, 2),
            ("Paula", 1994, 2),
            ("Ficciones", 1944, 3),
            ("El Aleph", 1949, 3),
        ]
        insertar_libros(conexion, libros)
        print("Libros insertados correctamente")

        print("\n--- Lista de todos los libros con sus autores ---")
        consultar_libros(conexion)

        print("\n--- Búsqueda de libros por autor ---")
        nombre_autor = "Gabriel García Márquez"
        libros_autor = buscar_libros_por_autor(conexion, nombre_autor)
        print(f"Libros de {nombre_autor}:")
        for titulo, anio in libros_autor:
            print(f"- {titulo} ({anio})")

        print("\n--- Actualización de un libro ---")
        actualizar_libro(
            conexion, 1, nuevo_titulo="Cien años de soledad (Edición especial)"
        )
        print("Libro actualizado. Nueva información:")
        consultar_libros(conexion)

        print("\n--- Eliminación de un libro ---")
        eliminar_libro(conexion, 6)  # Elimina "El Aleph"
        print("Libro eliminado. Lista actualizada:")
        consultar_libros(conexion)

        print("\n--- Demostración de transacción ---")
        ejemplo_transaccion(conexion)

    except sqlite3.Error as e:
        print(f"Error de SQLite: {e}")
    finally:
        if conexion:
            conexion.close()
            print("\nConexión cerrada.")
