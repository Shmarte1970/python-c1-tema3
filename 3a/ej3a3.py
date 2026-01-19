"""
Enunciado:
En este ejercicio aprenderás a trabajar con bases de datos SQLite existentes.
Aprenderás a:
1. Conectar a una base de datos SQLite existente
2. Convertir datos de SQLite a formatos compatibles con JSON
3. Extraer datos de SQLite a pandas DataFrame

El archivo ventas_comerciales.db contiene datos de ventas con tablas relacionadas
que incluyen productos, vendedores, regiones y ventas. Debes analizar estos datos
usando diferentes técnicas.
"""

import os
import sqlite3
from typing import Any, Dict, List

import pandas as pd

# Ruta a la base de datos SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), "ventas_comerciales.db")


def conectar_bd() -> sqlite3.Connection:
    """
    Conecta a una base de datos SQLite existente

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos SQLite
    """

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"No se encontró la base de datos en {DB_PATH}")

    conexion = sqlite3.connect(DB_PATH)

    conexion.row_factory = sqlite3.Row

    return conexion


def convertir_a_json(conexion: sqlite3.Connection) -> Dict[str, List[Dict[str, Any]]]:
    """
    Convierte los datos de la base de datos en un objeto compatible con JSON

    Args:
        conexion (sqlite3.Connection): Conexión a la base de datos SQLite

    Returns:
        Dict[str, List[Dict[str, Any]]]: Diccionario con todas las tablas y sus registros
        en formato JSON-serializable
    """
    resultado: Dict[str, List[Dict[str, Any]]] = {}

    cursor = conexion.cursor()

    # 1. Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = [fila[0] for fila in cursor.fetchall()]

    # 2. Procesar cada tabla
    for tabla in tablas:
        cursor.execute(f"SELECT * FROM {tabla}")
        filas = cursor.fetchall()

        # Obtener nombres de columnas
        columnas = [desc[0] for desc in cursor.description]

        registros = []
        for fila in filas:
            # Convertir fila a dict JSON-serializable
            registro = {col: fila[idx] for idx, col in enumerate(columnas)}
            registros.append(registro)

        resultado[tabla] = registros

    return resultado


def convertir_a_dataframes(conexion: sqlite3.Connection) -> Dict[str, pd.DataFrame]:
    """
    Extrae los datos de la base de datos a DataFrames de pandas

    Args:
        conexion (sqlite3.Connection): Conexión a la base de datos SQLite

    Returns:
        Dict[str, pd.DataFrame]: Diccionario con DataFrames para cada tabla y para
        consultas combinadas relevantes
    """
    dataframes: Dict[str, pd.DataFrame] = {}

    # 1. Obtener lista de tablas
    tablas_df = pd.read_sql_query(
        "SELECT name FROM sqlite_master WHERE type='table';", conexion
    )
    tablas = tablas_df["name"].tolist()

    # 2. DataFrames individuales por tabla
    for tabla in tablas:
        df = pd.read_sql_query(f"SELECT * FROM {tabla};", conexion)
        dataframes[tabla] = df

    # 3. DataFrames con JOINs relevantes

    # Ventas + productos
    df_ventas_productos = pd.read_sql_query(
        """
        SELECT v.*, p.nombre AS producto_nombre, p.categoria, p.precio_unitario
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
    """,
        conexion,
    )
    dataframes["ventas_productos"] = df_ventas_productos

    # Ventas + vendedores
    df_ventas_vendedores = pd.read_sql_query(
        """
        SELECT v.*, ve.nombre AS vendedor_nombre, ve.region_id
        FROM ventas v
        JOIN vendedores ve ON v.vendedor_id = ve.id
    """,
        conexion,
    )
    dataframes["ventas_vendedores"] = df_ventas_vendedores

    # Vendedores + regiones
    df_vendedores_regiones = pd.read_sql_query(
        """
        SELECT ve.*, r.nombre AS region_nombre, r.pais
        FROM vendedores ve
        JOIN regiones r ON ve.region_id = r.id
    """,
        conexion,
    )
    dataframes["vendedores_regiones"] = df_vendedores_regiones

    return dataframes


if __name__ == "__main__":
    try:
        # Conectar a la base de datos existente
        print("Conectando a la base de datos...")
        conexion = conectar_bd()
        print("Conexión establecida correctamente.")

        # Verificar la conexión mostrando las tablas disponibles
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        print(f"\nTablas en la base de datos: {[t[0] for t in tablas]}")

        # Conversión a JSON
        print("\n--- Convertir datos a formato JSON ---")
        datos_json = convertir_a_json(conexion)
        print("Estructura JSON (ejemplo de una tabla):")
        if datos_json:
            # Muestra un ejemplo de la primera tabla encontrada
            primera_tabla = list(datos_json.keys())[0]
            print(f"Tabla: {primera_tabla}")
            if datos_json[primera_tabla]:
                print(f"Primer registro: {datos_json[primera_tabla][0]}")

            # Opcional: guardar los datos en un archivo JSON
            # ruta_json = os.path.join(os.path.dirname(__file__), 'ventas_comerciales.json')
            # with open(ruta_json, 'w', encoding='utf-8') as f:
            #     json.dump(datos_json, f, ensure_ascii=False, indent=2)
            # print(f"Datos guardados en {ruta_json}")

        # Conversión a DataFrames de pandas
        print("\n--- Convertir datos a DataFrames de pandas ---")
        dataframes = convertir_a_dataframes(conexion)
        if dataframes:
            print(f"Se han creado {len(dataframes)} DataFrames:")
            for nombre, df in dataframes.items():
                print(f"- {nombre}: {len(df)} filas x {len(df.columns)} columnas")
                print(f"  Columnas: {', '.join(df.columns.tolist())}")
                print(f"  Vista previa:\n{df.head(2)}\n")

    except sqlite3.Error as e:
        print(f"Error de SQLite: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if "conexion" in locals() and conexion:
            conexion.close()
            print("\nConexión cerrada.")
