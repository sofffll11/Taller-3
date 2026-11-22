import random


def generar_registros(cantidad=50):
    """Crea la lista con los datos"""
    registros = []
    for i in range(1, cantidad + 1):
        registro = {
            "id": f"ID-{i:03d}",
            "fr": f"{random.randint(18, 90)} Años",
            "fc": f"{random.randint(50, 130):03d}ppm",
            "spo2": f"{random.randint(88, 100)}%",
        }
        registros.append(registro)
    return registros


def obtener_fc(registro):
    
    return int(registro["fc"].replace("ppm", ""))


def ordenar_por_fc(registros):
    
    datos = registros.copy()  
    n = len(datos)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if obtener_fc(datos[j]) > obtener_fc(datos[j + 1]):
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
    return datos