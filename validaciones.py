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

        


