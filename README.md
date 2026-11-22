# Taller-3

## Configurar MongoDB

Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```

Haz una copia de `.env.example` llamada `.env` y reemplaza los valores de ejemplo con los de MongoDB Atlas:

```env
MONGODB_URI=mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/
MONGODB_DB_NAME=<nombre_de_base_de_datos>
```

El módulo carga `.env` automáticamente. No guardes credenciales en el código ni subas `.env` al repositorio; ya está excluido por `.gitignore`. La URI debe corresponder a un usuario de base de datos de Atlas, y la IP desde la que ejecutas el programa debe estar permitida en la configuración de red de Atlas.

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
