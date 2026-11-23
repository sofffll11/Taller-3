**Curso:** Informática 1 — Universidad de Antioquia (Facultad de Ingeniería)  
**Unidades:** 3 y 4  
**Monitor:** Juan Esteban Pineda Lopera (`jesteban.pineda1@udea.edu.co`)

---

## 🎯 Objetivo General
Desarrollar competencias en estructuración de datos biomédicos, ordenamiento, manejo de archivos (.txt, .csv, .json), manipulación de directorios/rutas del sistema, validación mediante expresiones regulares e integración de Python con bases de datos NoSQL (MongoDB Atlas), así como el control de versiones con GitHub.

---

## 📋 Requerimientos y Puntos a Desarrollar

### 1. Procesamiento y Ordenamiento de Datos (15%)
- Generar al menos **50 registros biomédicos aleatorios**.
- Cada registro debe incluir exactamente los siguientes campos y formatos específicos:
  - `id`: Identificación con formato `"ID-XXX"` (ej. `"ID-001"`).
  - `fr`: Edad con formato `"XX Años"` (ej. `"18 Años"`).
  - `fc`: Frecuencia cardíaca con formato `"XXXppm"` (ej. `"090ppm"`).
  - `spo2`: Saturación periférica de oxígeno con formato `"XX%"` (ej. `"95%"`).
- Aplicar un algoritmo de ordenamiento para **ordenar los datos por el campo de frecuencia cardíaca (`fc`)**.

### 2. Gestión de Archivos: TXT, CSV y JSON (15%)
- **Guardar** los datos previamente ordenados en formatos `.txt` y `.csv`.
- **Exportar e importar** los datos en formato `.json`.
- Implementar **manejo de excepciones** (control de errores) y **verificación de rutas** de almacenamiento/lectura.

### 3. Herramientas del Sistema: `io`, `os`, `pathlib` (10%)
- Crear automáticamente la siguiente estructura de carpetas:
  - `/data/txt`
  - `/data/csv`
  - `/data/json`
- Mover y organizar automáticamente los archivos generados en sus respectivas carpetas.
- Generar un archivo `log.txt` donde se registren automáticamente las acciones y eventos realizados por el sistema.

### 4. Validación con Expresiones Regulares (10%)
- Al ingresar datos, verificar mediante **Expresiones Regulares (regex)** que cada campo de los registros (`id`, `fr`, `fc`, `spo2`) cumpla estrictamente con el patrón estipulado en el punto 1:
  - `id`: `^ID-\d{3}$`
  - `fr`: `^\d{2}\sAños$`
  - `fc`: `^\d{3}ppm$`
  - `spo2`: `^\d{2}\%$`

### 5. Gestión de Base de Datos NoSQL: MongoDB (25%)
- Establecer conexión entre Python y **MongoDB Atlas**.
- Crear una base de datos y una colección llamada `signos_vitales`.
- Insertar los registros previamente validados.
- Realizar y ejecutar las siguientes **consultas**:
  1. Calcular/consultar el **promedio de frecuencia cardíaca**.
  2. Consultar documentos cuya saturación de oxígeno ($SpO_2$) sea **menor a 94%**.
- Exportar los resultados de las consultas realizadas a un archivo `resultados_mongo.json`.

### 6. Integración Final del Sistema (15%)
- Crear un archivo principal denominado `main.py`.
- Diseñar un **menú interactivo** por consola que permita:
  1. Ingresar nuevos datos (con su respectiva validación regex).
  2. Exportar e importar archivos (`.txt`, `.csv`, `.json`).
  3. Validar datos existentes.
  4. Conectarse a MongoDB Atlas y ejecutar consultas específicas a través de un `ID`.

### 7. Uso de GitHub y Control de Versiones (10%)
- Crear un repositorio público en GitHub para permitir su revisión.
- Incluir el código fuente estructurado y la documentación del proyecto dentro de un archivo `README.md`.
- Registrar **al menos 5 commits** con mensajes claros y adecuados sobre el avance del desarrollo.

---

## 📊 Rúbrica de Evaluación

| Criterio / Ítem | Descripción | Porcentaje |
| :--- | :--- | :---: |
| **1. Procesamiento y ordenamiento** | Generación de 50+ datos y ordenamiento por $fc$. | **15%** |
| **2. Gestión de archivos** | Manejo de TXT, CSV, JSON, rutas y excepciones. | **15%** |
| **3. Herramientas del sistema** | Estructura de directorios, organización y `log.txt`. | **10%** |
| **4. Expresiones regulares** | Validación estricta de formato en cada campo. | **10%** |
| **5. Base de datos MongoDB** | Conexión Atlas, colección, consultas y exportación JSON. | **25%** |
| **6. Integración del sistema** | Menú interactivo en `main.py` funcional y completo. | **15%** |
| **7. GitHub y Control de versiones** | Repositorio público, `README.md` y 5+ commits adecuados. | **10%** |
| **TOTAL** | | **100%** |