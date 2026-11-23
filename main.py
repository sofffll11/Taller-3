from logging import error
from pathlib import Path
from re import error

import archivos
import mongoDB
from generador import generar_registros, ordenar_por_fc
from pymongo.errors import PyMongoError
from sistema import guardar_registros
from validaciones import _validar_registros, solicitarDato




def mostrar_menu():
    print("""\nSistema de datos biomédicos""")
    print("1. Generar 50 registros aleatorios")
    print("2. Exportar registros a JSON, CSV y TXT")
    print("3. Importar registros")
    print("4. Validar registros actuales")
    print("5. Insertar registros validados en MongoDB Atlas")
    print("6. Consultar un registro por ID")
    print("7. Consultas de frecuencia y SpO2; exportar resultados")
    print("0. Salir\n")


def _requiere_registros(registros):
    if not registros:
        print("No hay registros disponibles. Genere, importe o ingrese datos primero.")
        return False
    return True


def _con_cliente(funcion):
    cliente = mongoDB.crear_cliente()
    try:
        db = mongoDB.obtener_base_datos(cliente)
        return funcion(mongoDB.obtener_coleccion(db))
    finally:
        cliente.close()




def _mensaje_error(error):
    if isinstance(error, PyMongoError):
        codigo = getattr(error, "code", None)
        return f"Error de MongoDB ({type(error).__name__}, código {codigo}): {error}"
    return str(error)


def main():
    registros = []
    
    try:
        mongoDB.comprobar_conexion()
        print("Conexi?n con MongoDB Atlas correcta.")
        archivos.registrar_accion("Comprobaci?n inicial de MongoDB Atlas correcta")
    except (RuntimeError, PyMongoError, OSError) as error:
        print(f"Atlas no est? disponible ahora: {_mensaje_error(error)}")
        print("Puedes continuar usando las funciones locales del programa.")
        archivos.registrar_accion(f"Fallo la comprobacion inicial de Atlas: {type(error).__name__}")

    while True:
        mostrar_menu()
        opcion = solicitarDato("Seleccione una opcion: ", "int", 0, 7)
        try:
            if opcion == 0:

                print("Hasta luego.")
                break
            if opcion == 1:

                registros = ordenar_por_fc(generar_registros())
                print(f"Se generaron y ordenaron {len(registros)} registros.")
                archivos.registrar_accion(f"Generacion de {len(registros)} registros")
            elif opcion == 2:

                if _requiere_registros(registros):
                    registros = ordenar_por_fc(_validar_registros(registros))
                    rutas = guardar_registros(registros)
                    print("Archivos exportados:")
                    for ruta in rutas:
                        print(f"- {ruta}")

            elif opcion == 3:

                formato = solicitarDato("Formato: \n1) JSON, \n2) CSV, \n3) TXT \n", "int", 1, 3)
                importar = {1: archivos.importar_json, 2: archivos.importar_csv, 3: archivos.importar_txt}[formato]
                registros = ordenar_por_fc(importar())
                print(f"Se importaron {len(registros)} registros válidos.")

            elif opcion == 4:

                if _requiere_registros(registros):
                    registros = _validar_registros(registros)
                    print(f"Validacion correcta: {len(registros)} registros.")
                    archivos.registrar_accion(f"Validacion correcta de {len(registros)} registros")

            elif opcion == 5:

                if _requiere_registros(registros):
                    registros = _validar_registros(registros)
                    cantidad = _con_cliente(lambda c: mongoDB.insertar_registros(c, registros))
                    archivos.registrar_accion(f"Upsert de {cantidad} registros en Atlas")
                    print(f"Se guardaron {cantidad} registros en la coleccion '{mongoDB.COLECCION}'.")

            elif opcion == 6:

                numero_id = solicitarDato("Número de ID a consultar (ej. 30): ")

                if not numero_id.isdigit() or not 1 <= int(numero_id) <= 999:
                    raise ValueError("Ingrese un número entre 1 y 999.")

                identificacion = f"ID-{int(numero_id):03d}"
                documento = _con_cliente(
                    lambda coleccion: mongoDB.consultar_por_id(coleccion, identificacion)
                )

                if documento:
                    print("\n" + "─" * 32)
                    print("       SIGNOS VITALES")
                    print("─" * 32)
                    print(f"ID:                         {documento['id']}")
                    print(f"Frecuencia cardíaca:        {documento['fc']}")
                    print(f"Edad:                       {documento['fr']}")
                    print(f"Saturación de oxígeno:     {documento['spo2']}")
                    print("─" * 32)
                else:
                    print(f"No se encontró el registro {identificacion}.")
                archivos.registrar_accion(f"Consulta Atlas por ID {identificacion}")

            elif opcion == 7:

                ruta, resultados = _con_cliente(mongoDB.exportar_resultados)
                print(f"Promedio FC: {resultados['promedio_frecuencia_cardiaca_ppm']}")
                print(f"Registros con SpO2 menor a 94: {len(resultados['spo2_menor_a_94'])}")
                print(f"Resultados exportados a {ruta}")
                archivos.registrar_accion(f"Consultas Atlas exportadas a {ruta}")

        
                
        except (ValueError, OSError, PyMongoError, RuntimeError) as error:
            print(f"No se pudo completar la operacion: {_mensaje_error(error)}")
            detalle = type(error).__name__ if isinstance(error, PyMongoError) else str(error)
            archivos.registrar_accion(f"Operacion {opcion} fallida: {type(error).__name__}: {detalle}")


if __name__ == "__main__":
    main()
