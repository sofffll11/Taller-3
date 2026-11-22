import os

from pymongo import MongoClient
from pymongo.database import Database


"""
Utilidades de conexión a MongoDB.

Configura MONGODB_URI y MONGODB_DB_NAME en el entorno antes de usar el módulo.
Importar este archivo no abre una conexión; usa crear_cliente() explícitamente.
"""




def crear_cliente() -> MongoClient:
    """Crea un cliente MongoDB usando la URI configurada en el entorno."""
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise RuntimeError("Falta configurar la variable de entorno MONGODB_URI.")

    return MongoClient(uri, serverSelectionTimeoutMS=5000)


def obtener_base_datos(cliente: MongoClient) -> Database:
    """Devuelve la base de datos configurada para este proyecto."""
    nombre = os.getenv("MONGODB_DB_NAME")
    if not nombre:
        raise RuntimeError("Falta configurar la variable de entorno MONGODB_DB_NAME.")

    return cliente[nombre]


def comprobar_conexion() -> None:
    """Verifica la conexión y cierra el cliente al terminar."""
    cliente = crear_cliente()
    try:
        cliente.admin.command("ping")
        print("Conexión con MongoDB correcta.")
    finally:
        cliente.close()


if __name__ == "__main__":
    comprobar_conexion()
