"""
Enunciado:
En este ejercicio aprenderás a inicializar una base de datos SQLite a partir de un archivo SQL
y a realizar operaciones básicas de modificación de datos.
Aprenderás a:
1. Crear una base de datos SQLite a partir de un script SQL
2. Consultar datos usando SQL
3. Insertar nuevos registros en la base de datos
4. Actualizar registros existentes

El archivo test.sql contiene un script que crea una pequeña biblioteca con autores y libros.
Debes crear una base de datos a partir de este script y realizar operaciones sobre ella.
"""

import os
import sqlite3
from typing import List, Optional, Tuple

# Ruta al archivo SQL
SQL_FILE_PATH = os.path.join(os.path.dirname(__file__), "test.sql")
# Ruta para la base de datos SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), "biblioteca.db")


def crear_bd_desde_sql() -> sqlite3.Connection:
    """
    Crea una base de datos SQLite a partir del archivo SQL

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos SQLite
    """

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conexion = sqlite3.connect(DB_PATH)

    with open(SQL_FILE_PATH, "r", encoding="utf-8") as f:
        sql_script = f.read()

    conexion.executescript(sql_script)

    conexion.commit()

    return conexion


def obtener_libros(conexion: sqlite3.Connection) -> List[Tuple]:
    """
    Obtiene la lista de libros con información de sus autores

    Args:
        conexion (sqlite3.Connection): Conexión a la base de datos SQLite

    Returns:
        List[Tuple]: Lista de tuplas (id, titulo, anio, autor)
    """
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT libros.id, libros.titulo, libros.anio, autores.nombre
        FROM libros
        JOIN autores ON libros.autor_id = autores.id
        ORDER BY libros.id;
    """)
    return cursor.fetchall()


def agregar_libro(
    conexion: sqlite3.Connection, titulo: str, anio: int, autor_id: int
) -> int:
    """
    Agrega un nuevo libro a la base de datos

    Args:
        conexion (sqlite3.Connection): Conexión a la base de datos SQLite
        titulo (str): Título del libro
        anio (int): Año de publicación
        autor_id (int): ID del autor en la tabla autores

    Returns:
        int: ID del nuevo libro insertado
    """
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO libros (titulo, anio, autor_id) VALUES (?, ?, ?)",
        (titulo, anio, autor_id),
    )
    conexion.commit()
    return cursor.lastrowid


def actualizar_libro(
    conexion: sqlite3.Connection,
    libro_id: int,
    nuevo_titulo: Optional[str] = None,
    nuevo_anio: Optional[int] = None,
    nuevo_autor_id: Optional[int] = None,
) -> bool:
    """
    Actualiza la información de un libro existente

    Args:
        conexion (sqlite3.Connection): Conexión a la base de datos SQLite
        libro_id (int): ID del libro a actualizar
        nuevo_titulo (Optional[str], opcional): Nuevo título, o None para mantener el actual
        nuevo_anio (Optional[int], opcional): Nuevo año, o None para mantener el actual
        nuevo_autor_id (Optional[int], opcional): Nuevo ID de autor, o None para mantener el actual

    Returns:
        bool: True si se actualizó correctamente, False si no se encontró el libro
    """
    cursor = conexion.cursor()

    # Verificar que el libro existe
    cursor.execute("SELECT id FROM libros WHERE id = ?", (libro_id,))
    if cursor.fetchone() is None:
        return False

    campos = []
    valores = []

    if nuevo_titulo is not None:
        campos.append("titulo = ?")
        valores.append(nuevo_titulo)

    if nuevo_anio is not None:
        campos.append("anio = ?")
        valores.append(nuevo_anio)

    if nuevo_autor_id is not None:
        campos.append("autor_id = ?")
        valores.append(nuevo_autor_id)

    if not campos:
        return True  # Nada que actualizar, pero el libro existe

    valores.append(libro_id)

    query = f"""
        UPDATE libros
        SET {", ".join(campos)}
        WHERE id = ?
    """

    cursor.execute(query, valores)
    conexion.commit()

    return cursor.rowcount > 0


def obtener_autores(conexion: sqlite3.Connection) -> List[Tuple]:
    """
    Obtiene la lista de autores

    Args:
        conexion (sqlite3.Connection): Conexión a la base de datos SQLite

    Returns:
        List[Tuple]: Lista de tuplas (id, nombre)
    """
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM autores ORDER BY id;")
    return cursor.fetchall()


if __name__ == "__main__":
    try:
        # Crea la base de datos desde el archivo SQL
        print("Creando base de datos desde el archivo SQL...")
        conexion = crear_bd_desde_sql()
        print("Base de datos creada correctamente.")

        # Verificar la conexión mostrando las tablas disponibles
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        print(f"\nTablas en la base de datos: {[t[0] for t in tablas]}")

        # Mostrar los autores disponibles
        print("\n--- Autores disponibles ---")
        autores = obtener_autores(conexion)
        for autor_id, nombre in autores:
            print(f"ID: {autor_id} - {nombre}")

        # Mostrar los datos de libros y autores
        print("\n--- Libros y autores en la base de datos ---")
        libros = obtener_libros(conexion)
        for libro in libros:
            libro_id, titulo, anio, autor = libro
            print(f"ID: {libro_id} - {titulo} ({anio}) de {autor}")

        # Agregar un nuevo libro
        print("\n--- Agregar un nuevo libro ---")
        # Usar ID de autor válido según los datos mostrados anteriormente
        autor_id = 2  # Por ejemplo, Isabel Allende
        titulo_nuevo = "Violeta"
        anio_nuevo = 2022

        nuevo_id = agregar_libro(conexion, titulo_nuevo, anio_nuevo, autor_id)
        print(f"Libro agregado con ID: {nuevo_id}")

        # Mostrar la lista actualizada de libros
        print("\n--- Lista actualizada de libros ---")
        libros = obtener_libros(conexion)
        for libro in libros:
            libro_id, titulo, anio, autor = libro
            print(f"ID: {libro_id} - {titulo} ({anio}) de {autor}")

        # Actualizar un libro
        print("\n--- Actualizar un libro existente ---")
        # Usar ID de libro válido (por ejemplo, el que acabamos de insertar)
        libro_a_actualizar = nuevo_id
        nuevo_anio = 2023  # Corregir el año de publicación

        actualizado = actualizar_libro(
            conexion, libro_a_actualizar, nuevo_anio=nuevo_anio
        )
        if actualizado:
            print(f"Libro con ID {libro_a_actualizar} actualizado correctamente")
        else:
            print(f"No se pudo actualizar el libro con ID {libro_a_actualizar}")

        # Mostrar la lista final de libros
        print("\n--- Lista final de libros ---")
        libros = obtener_libros(conexion)
        for libro in libros:
            libro_id, titulo, anio, autor = libro
            print(f"ID: {libro_id} - {titulo} ({anio}) de {autor}")

    except sqlite3.Error as e:
        print(f"Error de SQLite: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if "conexion" in locals() and conexion:
            conexion.close()
            print("\nConexión cerrada.")
