import json
import os
from pathlib import Path

from pymongo import MongoClient, UpdateOne
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError


CARPETA_PROYECTO = Path(__file__).resolve().parent
ARCHIVO_CREDENCIALES = CARPETA_PROYECTO / "atlxas-credential.env"
if not ARCHIVO_CREDENCIALES.is_file():
    ARCHIVO_CREDENCIALES = CARPETA_PROYECTO / "atlas-credentials.env"

COLECCION = "signos_vitales"

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

def obtener_coleccion(db):
    """Devuelve la colección de signos vitales."""
    return db[COLECCION]


def insertar_registros(coleccion, registros):
    """Inserta o actualiza los registros usando su ID como clave."""
    if not registros:
        return 0

    operaciones = [
        UpdateOne(
            {"id": registro["id"]},
            {"$set": registro},
            upsert=True,
        )
        for registro in registros
    ]

    resultado = coleccion.bulk_write(operaciones, ordered=False)
    return resultado.upserted_count + resultado.modified_count


def consultar_por_id(coleccion, identificacion):
    """Busca un registro por su ID y oculta el identificador interno de MongoDB."""
    return coleccion.find_one(
        {"id": identificacion},
        {"_id": 0},
    )


def exportar_resultados(coleccion):
    """Calcula el promedio de FC, consulta SpO2 < 94 y guarda el resultado JSON."""
    pipeline = [
        {
            "$group": {
                "_id": None,
                "promedio": {
                    "$avg": {
                        "$convert": {
                            "input": {
                                "$replaceOne": {
                                    "input": "$fc",
                                    "find": "ppm",
                                    "replacement": "",
                                }
                            },
                            "to": "double",
                            "onError": None,
                            "onNull": None,
                        }
                    }
                },
            }
        }
    ]

    promedio_resultado = list(coleccion.aggregate(pipeline))
    promedio = (
        promedio_resultado[0]["promedio"]
        if promedio_resultado
        else None
    )

    documentos_bajos = list(
        coleccion.find(
            {
                "$expr": {
                    "$lt": [
                        {
                            "$convert": {
                                "input": {
                                    "$replaceOne": {
                                        "input": "$spo2",
                                        "find": "%",
                                        "replacement": "",
                                    }
                                },
                                "to": "int",
                                "onError": 1000,
                                "onNull": 1000,
                            }
                        },
                        94,
                    ]
                }
            },
            {"_id": 0},
        )
    )

    resultados = {
        "promedio_frecuencia_cardiaca_ppm": promedio,
        "spo2_menor_a_94": documentos_bajos,
    }

    carpeta_resultados = CARPETA_PROYECTO / "data"
    carpeta_resultados.mkdir(parents=True, exist_ok=True)
    ruta = carpeta_resultados / "resultados_mongo.json"

    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(resultados, archivo, ensure_ascii=False, indent=4)

    return ruta, resultados

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



COLECCION = "signos_vitales"
ARCHIVO_RESULTADOS = (
    Path(__file__).resolve().parent / "data" / "resultados_mongo.json"
)


def obtener_coleccion(db):
    """Devuelve la colección del taller."""
    return db[COLECCION]


def insertar_registros(coleccion, registros):
    """Inserta registros o actualiza los que ya tienen el mismo ID."""
    from pymongo import UpdateOne
    from validaciones import _validar_registros

    registros = _validar_registros(registros)

    if not registros:
        return 0

    operaciones = [
        UpdateOne(
            {"id": registro["id"]},
            {"$set": registro},
            upsert=True,
        )
        for registro in registros
    ]

    resultado = coleccion.bulk_write(operaciones, ordered=False)

    return resultado.upserted_count + resultado.modified_count


def consultar_por_id(coleccion, identificacion):
    """Busca un registro por su ID."""
    return coleccion.find_one(
        {"id": identificacion},
        {"_id": 0},
    )


def exportar_resultados(coleccion):
    """Calcula el promedio de FC y obtiene registros con SpO2 menor a 94."""
    pipeline_promedio = [
        {
            "$project": {
                "fc_num": {
                    "$toInt": {
                        "$substrBytes": ["$fc", 0, 3]
                    }
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "promedio": {"$avg": "$fc_num"},
            }
        },
    ]

    resultado_promedio = list(coleccion.aggregate(pipeline_promedio))

    if resultado_promedio:
        promedio = resultado_promedio[0]["promedio"]
    else:
        promedio = None

    registros_spo2_bajo = list(
        coleccion.find(
            {
                "$expr": {
                    "$lt": [
                        {
                            "$toInt": {
                                "$substrBytes": ["$spo2", 0, 2]
                            }
                        },
                        94,
                    ]
                }
            },
            {"_id": 0},
        )
    )

    resultados = {
        "promedio_frecuencia_cardiaca_ppm": promedio,
        "spo2_menor_a_94": registros_spo2_bajo,
    }

    ARCHIVO_RESULTADOS.parent.mkdir(parents=True, exist_ok=True)

    with ARCHIVO_RESULTADOS.open("w", encoding="utf-8") as archivo:
        json.dump(resultados, archivo, ensure_ascii=False, indent=2)

    return ARCHIVO_RESULTADOS, resultados


