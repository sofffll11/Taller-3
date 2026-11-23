import random

def generar_registros(cantidad=50):
    """Genera registros de ejemplo con el formato solicitado en el taller."""
    if cantidad < 50:
        raise ValueError("La consigna requiere generar al menos 50 registros.")

    return [
        {
            "id": f"ID-{i:03d}",
            "fr": f"{random.randint(18, 90)} Años",
            "fc": f"{random.randint(50, 130):03d}ppm",
            "spo2": f"{random.randint(88, 100)}%",
        }
        for i in range(1, cantidad + 1)
    ]


def obtener_fc(registro):
    return int(registro["fc"].removesuffix("ppm"))


def ordenar_por_fc(registros):
    """Retorna una copia ordenada num?ricamente por frecuencia cardiaca."""
    return sorted(registros, key=obtener_fc)
