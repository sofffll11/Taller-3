CAMPOS = ("id", "fr", "fc", "spo2")


def solicitarDato(mensaje, tipoDato, valorMinimo=None, valorMaximo=None):
    while True:

        entrada = input(mensaje).strip()

        if entrada == "":

            print("Error: No se puede dejar el campo vacío. Por favor, ingrese un valor.")
            continue

        if tipoDato == "int":

            try:

                valor = int(entrada)

                if valorMinimo is not None and valor < valorMinimo:

                    print(f"Error: El valor ingresado debe ser mayor o igual a {valorMinimo}. Por favor, intente nuevamente.")
                    continue

                if valorMaximo is not None and valor > valorMaximo:

                    print(f"Error: El valor ingresado debe ser menor o igual a {valorMaximo}. Por favor, intente nuevamente.")
                    continue
                

                return valor

            except ValueError:

                print("Error: Debe ingresar un número entero válido. Por favor, intente nuevamente.")
                continue

        elif tipoDato == "texto":

            try:
                float(entrada)
                print("Error: No se puede ingresar solo números. Por favor, ingrese un texto válido.")

            except ValueError:
                pass

            return entrada

def _validar_registros(registros):
    """Comprueba que cada elemento tenga los campos esperados."""
    if not isinstance(registros, list):
        raise ValueError("El archivo debe contener una lista de registros.")

    registros_validos = []

    for numero, registro in enumerate(registros, start=1):
        if not isinstance(registro, dict):
            raise ValueError(f"El registro {numero} no es un objeto válido.")

        faltantes = [campo for campo in CAMPOS if campo not in registro]
        if faltantes:
            raise ValueError(
                f"Al registro {numero} le faltan estos campos: "
                + ", ".join(faltantes)
            )

        registros_validos.append({
            campo: registro[campo]
            for campo in CAMPOS
        })

    return registros_validos

        


