import csv
import json
from pathlib import Path

from validaciones import _validar_registros


CARPETA_DATOS = Path(__file__).resolve().parent / "data"

def exportar_json(registros):
    registros = _validar_registros(registros)
    carpeta = CARPETA_DATOS / "json"
    carpeta.mkdir(parents=True, exist_ok=True)

    ruta = carpeta / "registros.json"
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=4)

    return ruta


def importar_json():
    ruta = CARPETA_DATOS / "json" / "registros.json"

    with ruta.open("r", encoding="utf-8-sig") as archivo:
        registros = json.load(archivo)

    return _validar_registros(registros)


def _exportar_tabla(registros, ruta, delimitador):
    registros = _validar_registros(registros)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=CAMPOS,
            delimiter=delimitador
        )
        escritor.writeheader()
        escritor.writerows(registros)

    return ruta


def _importar_tabla(ruta, delimitador):
    with ruta.open("r", newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo, delimiter=delimitador)

        if lector.fieldnames is None:
            raise ValueError(f"El archivo {ruta.name} está vacío.")

        faltantes = [campo for campo in CAMPOS if campo not in lector.fieldnames]
        if faltantes:
            raise ValueError(
                f"Al archivo {ruta.name} le faltan columnas: "
                + ", ".join(faltantes)
            )

        registros = list(lector)

    return _validar_registros(registros)


def exportar_csv(registros):
    ruta = CARPETA_DATOS / "csv" / "registros.csv"
    return _exportar_tabla(registros, ruta, delimitador=",")


def importar_csv():
    ruta = CARPETA_DATOS / "csv" / "registros.csv"
    return _importar_tabla(ruta, delimitador=",")


def exportar_txt(registros):
    ruta = CARPETA_DATOS / "txt" / "registros.txt"
    return _exportar_tabla(registros, ruta, delimitador=";")


def importar_txt():
    ruta = CARPETA_DATOS / "txt" / "registros.txt"
    return _importar_tabla(ruta, delimitador=";")


def exportar_todos(registros):
    rutas = [
        exportar_json(registros),
        exportar_csv(registros),
        exportar_txt(registros),
    ]
    return rutas