# Taller 3: Sistema de signos vitales

Proyecto de Informática 1 para generar, validar, ordenar, importar y exportar registros biomédicos, y trabajar con MongoDB Atlas.

## Requisitos

- Python 3.10 o posterior.
- MongoDB Atlas para las opciones que consultan o guardan información en la base de datos.
- Dependencias: `pymongo` y `dnspython`.

Instalación desde PowerShell, en la carpeta `Taller-3`:

```powershell
python -m pip install -r requirements.txt
```

## Configuración de MongoDB Atlas

El programa necesita las variables `MONGODB_URI` y `MONGODB_DB_NAME`. `mongoDB.py` carga esas variables desde `atlas-credentials.env` si el archivo está junto a `mongoDB.py`. También reconoce el nombre heredado `atlxas-credential.env` (con esa ortografía). El archivo `.env.example` es una plantilla; el código actual no carga automáticamente un archivo llamado `.env`.

Puedes copiar la plantilla con el nombre reconocido y completar los valores:

```powershell
Copy-Item .env.example atlas-credentials.env
```

Configura el acceso de red de Atlas para permitir la IP desde la que se ejecuta el programa. No publiques ni compartas la URI real del clúster.

La base de datos se elige con `MONGODB_DB_NAME` y la colección utilizada es `signos_vitales`.

## Ejecución

```powershell
python main.py
```

Al iniciar, el programa intenta comprobar la conexión con Atlas. Si Atlas no está disponible, informa el problema y permite continuar con las funciones locales. El menú ofrece:

1. Generar 50 registros biomédicos aleatorios.
2. Exportar los registros actuales a JSON, CSV y TXT.
3. Importar registros desde uno de esos formatos.
4. Validar los registros actuales.
5. Insertar o actualizar registros validados en Atlas.
6. Consultar un registro de Atlas por ID (actualmente solicita el formato `ID-XXX`, por ejemplo `ID-030`).
7. Calcular el promedio de frecuencia cardíaca y consultar registros con SpO2 menor que 94%; exporta el resultado JSON.

Los registros se ordenan por frecuencia cardíaca antes de exportarse o importarse al estado actual del programa. La opción de inserción valida los datos antes de guardarlos.

## Archivos generados

- `data/json/registros.json`: registros en JSON.
- `data/csv/registros.csv`: registros delimitados por comas.
- `data/txt/registros.txt`: registros delimitados por punto y coma.
- `data/resultados_mongo.json`: promedio de frecuencia cardíaca y registros con SpO2 inferior a 94%.
- `data/log.txt`: eventos y acciones del programa.

Las carpetas de datos se crean automáticamente. Los formatos de los campos se comprueban con expresiones regulares antes de exportar, importar o insertar.

## Módulos

- `main.py`: menú de consola y flujo principal.
- `generador.py`: generación de registros y ordenamiento por FC.
- `validaciones.py`: patrones y validación de campos.
- `archivos.py`: importación, exportación y registro de eventos.
- `sistema.py`: punto de entrada para guardar los tres formatos.
- `mongoDB.py`: conexión a Atlas, inserción/actualización y consultas.

## Estado frente al taller

La generación de al menos 50 registros, el ordenamiento por FC, los formatos TXT/CSV/JSON, la validación, las carpetas y el log están implementados. También están implementadas la conexión a Atlas, la escritura en `signos_vitales`, la consulta por ID, el promedio de FC, el filtro de SpO2 menor que 94% y la exportación de resultados.

Quedan pendientes dos detalles de la consigna: el menú no incluye una opción para ingresar un registro manualmente y la consulta por ID todavía solicita `ID-XXX` en vez de aceptar un número. La validación de SpO2 acepta valores de 88% a 100%, mientras que el patrón literal del documento especifica dos dígitos; el valor 100% requiere que la consigna defina una excepción.
