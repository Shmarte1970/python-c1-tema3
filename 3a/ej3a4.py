"""
Enunciado:
En este ejercicio aprenderás a utilizar MongoDB con Python para trabajar
con bases de datos NoSQL. MongoDB es una base de datos orientada a documentos que
almacena datos en formato similar a JSON (BSON).

Tareas:
1. Conectar a una base de datos MongoDB
2. Crear colecciones (equivalentes a tablas en SQL)
3. Insertar, actualizar, consultar y eliminar documentos
4. Manejar transacciones y errores

Este ejercicio se enfoca en las operaciones básicas de MongoDB desde Python utilizando PyMongo.
"""

import os
import subprocess
import sys
import time
from typing import List, Optional, Tuple

import pymongo
from bson.objectid import ObjectId

# Configuración de MongoDB (la debes obtener de "docker-compose.yml"):
DB_NAME = "biblioteca"
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_USERNAME = "testuser"
MONGODB_PASSWORD = "testpass"
MONGODB_AUTH_SOURCE = "admin"


def verificar_docker_instalado() -> bool:
    """
    Verifica si Docker está instalado en el sistema y el usuario tiene permisos
    """
    try:
        # Verificar si docker está instalado
        result = subprocess.run(
            ["docker", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            return False

        # Verificar si docker-compose está instalado
        result = subprocess.run(
            ["docker", "compose", "version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            return False

        # Verificar permisos de Docker
        result = subprocess.run(
            ["docker", "ps"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def iniciar_mongodb_docker() -> bool:
    """
    Inicia MongoDB usando Docker Compose
    """
    try:
        # Obtener la ruta al directorio actual donde está el docker-compose.yml
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Detener cualquier contenedor previo
        subprocess.run(
            ["docker", "compose", "down"],
            cwd=current_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

        # Iniciar MongoDB con docker-compose
        result = subprocess.run(
            ["docker", "compose", "up", "-d"],
            cwd=current_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            print(f"Error al iniciar MongoDB: {result.stderr}")
            return False

        # Dar tiempo para que MongoDB se inicie completamente
        time.sleep(5)
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar Docker Compose: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False


def detener_mongodb_docker() -> None:
    """
    Detiene el contenedor de MongoDB
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.run(
            ["docker", "compose", "down"],
            cwd=current_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except Exception as e:
        print(f"Error al detener MongoDB: {e}")


def crear_conexion() -> pymongo.database.Database:
    """
    Crea y devuelve una conexión a la base de datos MongoDB
    """
    client = pymongo.MongoClient(
        host=MONGODB_HOST,
        port=MONGODB_PORT,
        username=MONGODB_USERNAME,
        password=MONGODB_PASSWORD,
        authSource=MONGODB_AUTH_SOURCE
    )
    return client[DB_NAME]


def crear_colecciones(db: pymongo.database.Database) -> None:
    """
    Crea las colecciones necesarias para la biblioteca.
    En MongoDB, no es necesario definir el esquema de antemano,
    pero podemos crear índices para optimizar el rendimiento.
    """
    try:
        db.autores.create_index("nombre", unique=True)
        db.libros.create_index("titulo")
        db.libros.create_index("autor_id")
    except pymongo.errors.OperationFailure:
        # MongoDB con autenticación activa
        # No es crítico para el ejercicio
        pass


def insertar_autores(
    db: pymongo.database.Database, autores: List[Tuple[str]]
) -> List[str]:
    """
    Inserta varios autores en la colección 'autores'
    """
    documentos = [{"nombre": autor[0]} for autor in autores]

    result = db.autores.insert_many(documentos)

    return [str(_id) for _id in result.inserted_ids]


def insertar_libros(
    db: pymongo.database.Database, libros: List[Tuple[str, int, str]]
) -> List[str]:
    """
    Inserta varios libros en la colección 'libros'
    """
    documentos = []
    for titulo, anio, autor_id in libros:
        documentos.append(
            {"titulo": titulo, "anio": anio, "autor_id": ObjectId(autor_id)}
        )

    result = db.libros.insert_many(documentos)
    return [str(_id) for _id in result.inserted_ids]


def consultar_libros(db: pymongo.database.Database) -> None:
    """
    Consulta todos los libros y muestra título, año y nombre del autor
    """
    pipeline = [
        {
            "$lookup": {
                "from": "autores",
                "localField": "autor_id",
                "foreignField": "_id",
                "as": "autor",
            }
        },
        {"$unwind": "$autor"},
    ]

    for doc in db.libros.aggregate(pipeline):
        print(f"{doc['titulo']} ({doc['anio']}) - {doc['autor']['nombre']}")


def buscar_libros_por_autor(
    db: pymongo.database.Database, nombre_autor: str
) -> List[Tuple[str, int]]:
    """
    Busca libros por el nombre del autor
    """
    autor = db.autores.find_one({"nombre": nombre_autor})
    if not autor:
        return []

    libros = db.libros.find({"autor_id": autor["_id"]})

    return [(libro["titulo"], libro["anio"]) for libro in libros]


def actualizar_libro(
    db: pymongo.database.Database,
    id_libro: str,
    nuevo_titulo: Optional[str] = None,
    nuevo_anio: Optional[int] = None,
) -> bool:
    """
    Actualiza la información de un libro existente
    """
    cambios = {}

    if nuevo_titulo is not None:
        cambios["titulo"] = nuevo_titulo
    if nuevo_anio is not None:
        cambios["anio"] = nuevo_anio

    if not cambios:
        return False

    result = db.libros.update_one({"_id": ObjectId(id_libro)}, {"$set": cambios})

    return result.matched_count > 0


def eliminar_libro(db: pymongo.database.Database, id_libro: str) -> bool:
    """
    Elimina un libro por su ID
    """
    result = db.libros.delete_one({"_id": ObjectId(id_libro)})
    return result.deleted_count == 1


def ejemplo_transaccion(db: pymongo.database.Database) -> bool:
    """
    Demuestra el uso de operaciones agrupadas
    """
    try:
        autor = {"nombre": "Autor Transacción"}
        autor_id = db.autores.insert_one(autor).inserted_id

        libros = [
            {"titulo": "Libro Transacción 1", "anio": 2020, "autor_id": autor_id},
            {"titulo": "Libro Transacción 2", "anio": 2021, "autor_id": autor_id},
        ]

        db.libros.insert_many(libros)
        return True

    except Exception:
        # Limpieza manual si algo falla
        db.autores.delete_one({"_id": autor_id})
        db.libros.delete_many({"autor_id": autor_id})
        return False


if __name__ == "__main__":
    mongodb_proceso = None
    db = None

    try:
        # Verificar si Docker está instalado
        if not verificar_docker_instalado():
            print("Error: Docker no está instalado o no está disponible en el PATH.")
            print("Por favor, instala Docker y asegúrate de que esté en tu PATH.")
            sys.exit(1)

        # Iniciar MongoDB usando Docker
        print("Iniciando MongoDB con Docker...")
        if not iniciar_mongodb_docker():
            print(
                "No se pudo iniciar MongoDB. Asegúrate de tener los permisos necesarios."
            )
            sys.exit(1)

        print("MongoDB iniciado correctamente.")

        # Crear una conexión
        print("Conectando a MongoDB...")
        db = crear_conexion()
        print("Conexión establecida correctamente.")

        # Crear colecciones
        print("Creando colecciones...")
        crear_colecciones(db)
        print("Colecciones creadas correctamente.")

        # Insertar autores de prueba
        print("\nInsertando autores...")
        autores_lista = [
            ("Gabriel García Márquez",),
            ("Isabel Allende",),
            ("Jorge Luis Borges",),
        ]
        ids_autores = insertar_autores(db, autores_lista)
        print(f"Autores insertados con IDs: {ids_autores}")

        # Insertar libros de prueba
        print("\nInsertando libros...")
        libros_lista = [
            ("Cien años de soledad", 1967, ids_autores[0]),
            ("La casa de los espíritus", 1982, ids_autores[1]),
            ("El Aleph", 1949, ids_autores[2]),
            ("Violeta", 2022, ids_autores[1]),
        ]
        ids_libros = insertar_libros(db, libros_lista)
        print(f"Libros insertados con IDs: {ids_libros}")

        # Consultar todos los libros
        print("\n--- Todos los libros ---")
        consultar_libros(db)

        # Buscar libros por autor
        print("\n--- Libros de Isabel Allende ---")
        libros_allende = buscar_libros_por_autor(db, "Isabel Allende")
        for titulo, anio in libros_allende:
            print(f"{titulo} ({anio})")

        # Actualizar un libro
        print("\n--- Actualizar libro ---")
        actualizado = actualizar_libro(
            db, ids_libros[0], nuevo_titulo="Cien años de soledad (Edición revisada)"
        )
        if actualizado:
            print("Libro actualizado correctamente")

        # Eliminar un libro
        print("\n--- Eliminar libro ---")
        eliminado = eliminar_libro(db, ids_libros[-1])
        if eliminado:
            print("Libro eliminado correctamente")

        # Ejemplo de transacción
        print("\n--- Ejemplo de transacción ---")
        if ejemplo_transaccion(db):
            print("Transacción completada correctamente")

        # Mostrar libros finales
        print("\n--- Libros finales ---")
        consultar_libros(db)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cerrar la conexión a MongoDB
        if db is not None:
            print("\nConexión a MongoDB cerrada.")

        # Detener el proceso de MongoDB si lo iniciamos nosotros
        if mongodb_proceso:
            print("Deteniendo MongoDB...")
            detener_mongodb_docker()

            print("MongoDB detenido correctamente.")
