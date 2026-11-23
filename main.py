from generador import generar_registros, ordenar_por_fc
from validaciones import solicitarDato






def mostrar_menu():
    print("""Bienvenidos al sistema de datos biomédicos; seleccione una opción:\n""")
    print ("1.Generar registros aleatorios")
    print("2. Exportar archivos")
    print("3. Importar JSON")
    print("4. Validar registros")
    print("5. Insertar en MongoDB")
    print("6. Consultar por ID")
    print("7. Ejecutar consultas y exportar resultados")
    print("0. Salir")


def main():
    while True:
        mostrar_menu()
        opcion=solicitarDato("Ingrese el número de la opción deseada: ", "int", 0, 7)

        if opcion == 1:

        
            registros = generar_registros()
            print(f"{len(registros)} registros generados exitosamente.")

        elif opcion == 2: