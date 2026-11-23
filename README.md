# Taller 3 - Inform?tica 1

Sistema de ejemplo para generar, validar, ordenar, importar/exportar e insertar signos vitales en MongoDB Atlas.

## Requisitos

- Python 3.10 o posterior.
- Una base de datos MongoDB Atlas con acceso de red habilitado para tu IP.

Instala la dependencia:

```powershell
python -m pip install -r requirements.txt
```

## Configuraci?n de Atlas

Copia `.env.example` como `.env` y configura `MONGODB_URI` y `MONGODB_DB_NAME` con los valores de tu cl?ster. El archivo `.env` est? excluido por `.gitignore`; no publiques credenciales. Tambi?n se reconocen los nombres de archivo `atlas-credentials.env` y `atlas-credential.env` para conservar configuraciones previas. Si usas uno de esos archivos existentes, agrega all? `MONGODB_DB_NAME=<nombre exacto de tu base>`; la URI sola no indica con certeza qu? base debe usar el programa.

La colecci?n usada por el programa es `signos vitales`. La IP de ejecuci?n debe estar permitida en Network Access de Atlas.

## Ejecuci?n

```powershell
python main.py
```

El men? permite generar al menos 50 registros, exportar JSON/CSV/TXT, importar cualquiera de esos formatos, validar, insertar o consultar datos en Atlas e ingresar registros manualmente. Los datos se ordenan por frecuencia cardiaca antes de exportarse. Las acciones quedan registradas en `data/log.txt`.

Las exportaciones quedan en `data/json`, `data/csv` y `data/txt`. La opci?n de consultas guarda `data/resultados mongo.json` con el promedio de frecuencia cardiaca y los documentos con SpO2 menor a 94.

## Estructura principal

- `main.py`: men? e integraci?n.
- `generador.py`: generaci?n y ordenamiento.
- `validaciones.py`: validaci?n de campos y patrones.
- `archivos.py`: importaci?n, exportaci?n y registro de acciones.
- `mongoDB.py`: conexi?n, inserci?n y consultas de Atlas.
