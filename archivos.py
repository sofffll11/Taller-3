import csv
import json
import logging
from pathlib import Path

from validaciones import CAMPOS, _validar_registros

CARPETA_DATOS = Path(__file__).resolve().parent / "data"
CARPETA_JSON = CARPETA_DATOS / "json"
ARCHIVO_LOG = CARPETA_DATOS / "log.txt"


def registrar_accion(mensaje):
    """Registra una acci?n en data/log.txt."""
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=ARCHIVO_LOG,
        encoding="utf-8",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logging.info(mensaje)


def exportar_json(registros):
    registros = _validar_registros(registros)
    carpeta = CARPETA_JSON
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / "registros.json"
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=4)
    registrar_accion(f"Exportaci?n JSON: {len(registros)} registros -> {ruta}")
    return ruta


def importar_json():
    ruta = CARPETA_JSON / "registros.json"
    with ruta.open("r", encoding="utf-8-sig") as archivo:
        registros = json.load(archivo)
    registros = _validar_registros(registros)
    registrar_accion(f"Importaci?n JSON: {len(registros)} registros <- {ruta}")
    return registros


def _exportar_tabla(registros, ruta, delimitador):
    registros = _validar_registros(registros)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS, delimiter=delimitador)
        escritor.writeheader()
        escritor.writerows(registros)
    registrar_accion(f"Exportaci?n tabular: {len(registros)} registros -> {ruta}")
    return ruta


def _importar_tabla(ruta, delimitador):
    with ruta.open("r", newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo, delimiter=delimitador)
        if lector.fieldnames is None:
            raise ValueError(f"El archivo {ruta.name} est? vac?o.")
        faltantes = [campo for campo in CAMPOS if campo not in lector.fieldnames]
        if faltantes:
            raise ValueError(
                f"Al archivo {ruta.name} le faltan columnas: " + ", ".join(faltantes)
            )
        registros = list(lector)
    registros = _validar_registros(registros)
    registrar_accion(f"Importaci?n tabular: {len(registros)} registros <- {ruta}")
    return registros


def exportar_csv(registros):
    return _exportar_tabla(registros, CARPETA_DATOS / "csv" / "registros.csv", ",")


def importar_csv():
    return _importar_tabla(CARPETA_DATOS / "csv" / "registros.csv", ",")


def exportar_txt(registros):
    return _exportar_tabla(registros, CARPETA_DATOS / "txt" / "registros.txt", ";")


def importar_txt():
    return _importar_tabla(CARPETA_DATOS / "txt" / "registros.txt", ";")


def exportar_todos(registros):
    registros = _validar_registros(registros)
    return [exportar_json(registros), exportar_csv(registros), exportar_txt(registros)]
