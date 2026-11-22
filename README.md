# Taller-3

## Configurar MongoDB

Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```

Define las variables de entorno en PowerShell antes de ejecutar el proyecto:

```powershell
$env:MONGODB_URI = "mongodb+srv://<usuario>:<contraseña>@<cluster>/"
$env:MONGODB_DB_NAME = "<nombre_de_base_de_datos>"
```

No guardes credenciales en el código ni subas valores reales al repositorio. La URI debe corresponder a un usuario de base de datos de Atlas, y la IP desde la que ejecutas el programa debe estar permitida en la configuración de red de Atlas.

## Uso desde Python

```python
from mongoDB import crear_cliente, obtener_base_datos

cliente = crear_cliente()
try:
    db = obtener_base_datos(cliente)
    coleccion = db["registros"]
    # Usa coleccion para consultar o guardar documentos.
finally:
    cliente.close()
```

Para comprobar la conexión manualmente, configura las variables anteriores y ejecuta `python mongoDB.py`. Importar `mongoDB.py` por sí solo no inicia conexiones.
