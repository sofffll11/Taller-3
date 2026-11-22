import random


def generar_registros(cantidad=50):
    """Crea una lista de registros biomédicos aleatorios."""
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