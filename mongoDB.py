"""Conexión de prueba y acceso a la base de datos de MongoDB Atlas."""

import os
from pathlib import Path

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError


CARPETA_PROYECTO = Path(__file__).resolve().parent
ARCHIVO_CREDENCIALES = CARPETA_PROYECTO / "atlas-credential.env"
if not ARCHIVO_CREDENCIALES.is_file():
    ARCHIVO_CREDENCIALES = CARPETA_PROYECTO / "atlas-credentials.env"

def cargar_credenciales() -> None:
    """Lee KEY=VALUE del archivo sin requerir paquetes externos adicionales."""
    if not ARCHIVO_CREDENCIALES.is_file():
        return

    for linea in ARCHIVO_CREDENCIALES.read_text(encoding="utf-8-sig").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue

        clave, valor = linea.split("=", 1)
        clave = clave.strip()
        valor = valor.strip()
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in ("'", '"'):
            valor = valor[1:-1]
        if clave:
            os.environ.setdefault(clave, valor)


cargar_credenciales()


def crear_cliente() -> MongoClient:
    """Crea un cliente Atlas usando MONGODB_URI."""
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise RuntimeError(
            f"No se encontró MONGODB_URI en {ARCHIVO_CREDENCIALES.name}. "
            "Verifica que el archivo esté junto a mongoDB.py y que la línea "
            "tenga el formato MONGODB_URI=mongodb+srv://..."
        )

    # mongodb+srv normalmente habilita TLS automáticamente; se deja explícito.
    return MongoClient(
        uri,
        tls=True,
        serverSelectionTimeoutMS=15000,
        connectTimeoutMS=10000,
    )


def obtener_base_datos(cliente: MongoClient) -> Database:
    """Devuelve la base nombrada en MONGODB_DB_NAME."""
    nombre = os.getenv("MONGODB_DB_NAME")
    if not nombre:
        raise RuntimeError(
            f"Falta MONGODB_DB_NAME en {ARCHIVO_CREDENCIALES.name}; "
            "agrega, por ejemplo, MONGODB_DB_NAME=taller3."
        )
    return cliente[nombre]


def comprobar_conexion() -> None:
    """Hace ping a Atlas y cierra el cliente incluso si la conexión falla."""
    cliente = crear_cliente()
    try:
        cliente.admin.command("ping")
        print("Conexión con MongoDB Atlas correcta.")
    except ServerSelectionTimeoutError as error:
        print(
            "No se pudo completar la conexión TLS con Atlas. Comprueba que el "
            "clúster esté activo, que tu IP esté permitida en Network Access y "
            "que VPN, proxy o firewall no bloqueen la conexión saliente TCP "
            "a los puertos 27015–27017."
        )
        raise error
    finally:
        cliente.close()


if __name__ == "__main__":
    comprobar_conexion()
