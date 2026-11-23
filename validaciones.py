import re

CAMPOS = ("id", "fr", "fc", "spo2")
PATRONES = {
    "id": re.compile(r"^ID-\d{3}$"),
    "fr": re.compile(r"^\d{2}\sAños$"),
    "fc": re.compile(r"^\d{3}ppm$"),
    "spo2": re.compile(r"^\d{2}\%$"),
}


def solicitarDato(mensaje, tipoDato="texto", valorMinimo=None, valorMaximo=None):
    """Solicita un dato simple y vuelve a preguntar si no cumple el tipo."""
    while True:
        entrada = input(mensaje).strip()
        if not entrada:
            print("Error: el campo no puede quedar vac?o.")
            continue

        if tipoDato == "int":
            try:
                valor = int(entrada)
            except ValueError:
                print("Error: ingrese un n?mero entero v?lido.")
                continue
            if valorMinimo is not None and valor < valorMinimo:
                print(f"Error: el valor debe ser mayor o igual a {valorMinimo}.")
                continue
            if valorMaximo is not None and valor > valorMaximo:
                print(f"Error: el valor debe ser menor o igual a {valorMaximo}.")
                continue
            return valor

        if tipoDato == "texto":
            return entrada

        raise ValueError(f"Tipo de dato no soportado: {tipoDato}")


def _validar_registros(registros):
    """Comprueba estructura, presencia y formato de cada campo."""
    if not isinstance(registros, list):
        raise ValueError("Los registros deben estar dentro de una lista.")

    registros_validos = []
    for numero, registro in enumerate(registros, start=1):
        if not isinstance(registro, dict):
            raise ValueError(f"El registro {numero} no es un objeto v?lido.")

    campos_recibidos = set(registro.keys())
    campos_esperados = set(CAMPOS)

    faltantes = campos_esperados - campos_recibidos
    adicionales = campos_recibidos - campos_esperados

    if faltantes or adicionales:
        detalles = []

        if faltantes:
            detalles.append("faltan: " + ", ".join(sorted(faltantes)))

        if adicionales:
            detalles.append("sobran: " + ", ".join(sorted(adicionales)))

        raise ValueError(
            f"El registro {numero} debe tener exactamente los campos "
            f"{', '.join(CAMPOS)}; " + "; ".join(detalles)
        )

        normalizado = {}
        for campo in CAMPOS:
            valor = registro[campo]
            if not isinstance(valor, str) or PATRONES[campo].fullmatch(valor) is None:
                raise ValueError(
                    f"Registro {numero}: {campo}={valor!r} no cumple el formato esperado."
                )
            normalizado[campo] = valor
        registros_validos.append(normalizado)

    return registros_validos
