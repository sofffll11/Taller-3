from generador import generar_registros, ordenar_por_fc
from validaciones import solicitarDato
from sistema import guardar_registro
import archivos

def mostrar_menu():
    print("""Bienvenidos al sistema de datos biomédicos; seleccione una opción:\n""")
    print("1. Generar registros aleatorios")
    print("2. Exportar archivos")
    print("3. Importar archivos")
    print("4. Validar registros")
    print("5. Insertar registros validos en MongoDB")
    print("6. Consultar por ID")
    print("7. Realizar consultas y exportar resultados")
    print("0. Salir")


def main():

    registros: list[dict[str, str]] = []    
    
    while True:
        mostrar_menu()
        
        # Validación de la opción ingresada
        opcion = solicitarDato("\nIngrese el número de la opción deseada: ", "int", 0, 7)

        # Guardar registros y salir del programa
        if opcion == 0:

            for registro in registros:
                guardar_registro(registro)
            print("Saliendo del programa. ¡Hasta luego!")
            break

        # Generar registros aleatorios
        if opcion == 1:

        
            registros = generar_registros()
            print(f"\n{len(registros)} registros generados exitosamente.")

        # Exportar archivos
        elif opcion == 2:

            if 'registros' not in locals():
                print("\nNo hay registros generados. Por favor, genere registros primero.")
                continue

            for registro in registros:
                guardar_registro(registro)
            print("Registros exportados exitosamente.")

        # Importar archivos
        elif opcion == 3:

            print("\nSeleccione el formato de archivo a importar: \n")
            print("1. JSON")
            print("2. CSV")
            print("3. TXT\n")

            formato = solicitarDato("Ingrese el número del formato deseado: ", "int", 1, 3)

            if formato == 1:
                registros = archivos.importar_json()
                print(f"\n{len(registros)} registros importados desde JSON.")

            elif formato == 2:
                registros = archivos.importar_csv()
                print(f"\n{len(registros)} registros importados desde CSV.")

            elif formato == 3:
                registros = archivos.importar_txt()
                print(f"\n{len(registros)} registros importados desde TXT.")

        # Validar registros
        elif opcion == 4:
            if 'registros' not in locals():
                print("\nNo hay registros generados o importados. Por favor, genere o importe registros primero.")
                continue

            try:
                registros = archivos._validar_registros(registros)
                print("\nTodos los registros son válidos.")
            except ValueError as e:
                print(f"\nError de validación: {e}")

            


if __name__ == "__main__":
    main()