import archivos

def guardar_registro(registro):
    archivos.exportar_json(registro)
    archivos.exportar_csv(registro)
    archivos.exportar_txt(registro)