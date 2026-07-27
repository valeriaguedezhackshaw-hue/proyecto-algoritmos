"""modulo para cargar los datos iniciales de las localidades"""

import json

from modelos.municipio import Municipio
from modelos.localidad import Localidad


def cargar_municipios(ruta_archivo):
    """lee el archivo json y retorna una lista de objetos municipio"""
    archivo = open(ruta_archivo, "r", encoding="utf-8")
    datos = json.load(archivo)
    archivo.close()

    municipios = []
    for nombre_municipio in datos:
        municipio = Municipio(nombre_municipio)
        for localidad_datos in datos[nombre_municipio]:
            localidad = Localidad(
                localidad_datos["localidad"],
                localidad_datos["latitud"],
                localidad_datos["longitud"]
            )
            municipio.agregar_localidad(localidad)
        municipios.append(municipio)

    return municipios


def mostrar_reporte_carga(municipios):
    """muestra en pantalla el reporte de carga por cada municipio"""
    for municipio in municipios:
        print("municipio:", municipio.nombre)
        print("cantidad de localidades cargadas:", municipio.contar_localidades())
        print("cantidad con coordenadas:", municipio.contar_con_coordenadas())
        print("cantidad sin coordenadas:", municipio.contar_sin_coordenadas())
        print("porcentaje con coordenadas: {:.2f}%".format(municipio.porcentaje_con_coordenadas()))
        print()
