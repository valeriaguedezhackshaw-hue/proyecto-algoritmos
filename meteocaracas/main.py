"""programa principal del sistema meteocaracas"""

import os

from servicios.carga_datos import cargar_municipios, mostrar_reporte_carga
from servicios.busqueda import (
    listar_localidades_con_coordenadas,
    buscar_localidad_por_nombre
)
from servicios.clima_api import consultar_clima_actual
from servicios.estadisticas import (
    mostrar_ranking_temperatura,
    promedio_general,
    mostrar_cobertura_geografica
)
from servicios.historicos import (
    consultar_historico,
    resumen_mensual,
    mostrar_resumen_mensual,
    promedios_generales,
    resumen_anual,
    años_destacados,
    graficar_evolucion_anual
)


def imprimir_separador():
    """imprime una linea separadora para ordenar la salida en pantalla"""
    print("-" * 40)


def mostrar_menu():
    """muestra las opciones del menu principal"""
    imprimir_separador()
    print("----- meteocaracas -----")
    print("1. consultar clima por municipio y localidad")
    print("2. buscar clima por nombre de localidad")
    print("3. ver ranking de temperatura de la sesion")
    print("4. ver promedio general de la sesion")
    print("5. ver cobertura geografica")
    print("6. consultar clima historico por periodo")
    print("0. salir")
    imprimir_separador()


def mostrar_clima(municipio, localidad):
    """consulta y muestra el clima actual de una localidad, retorna la temperatura"""
    print("consultando clima de", localidad.nombre, "...")
    try:
        clima = consultar_clima_actual(localidad.latitud, localidad.longitud)
    except Exception:
        print("no se pudo consultar el clima, intenta de nuevo mas tarde")
        return None

    imprimir_separador()
    print("municipio:", municipio.nombre)
    print("localidad:", localidad.nombre)
    print("coordenadas:", localidad.latitud, localidad.longitud)
    print("temperatura actual:", clima.temperatura, "c")
    print("humedad relativa:", clima.humedad, "%")
    print("velocidad del viento:", clima.viento, "km/h")
    print("estado del tiempo:", clima.estado_tiempo)
    imprimir_separador()

    return clima.temperatura


def seleccionar_localidad(municipios):
    """muestra el selector de municipio y localidad y retorna la pareja elegida"""
    imprimir_separador()
    print("municipios disponibles:")
    contador = 1
    for municipio in municipios:
        print(contador, "-", municipio.nombre)
        contador += 1
    imprimir_separador()

    try:
        opcion = int(input("selecciona el numero del municipio: "))
    except ValueError:
        print("opcion invalida")
        return None, None

    if opcion < 1 or opcion > len(municipios):
        print("opcion invalida")
        return None, None

    municipio = municipios[opcion - 1]

    localidades = listar_localidades_con_coordenadas(municipio)
    if len(localidades) == 0:
        print("este municipio no tiene localidades con coordenadas validas")
        return None, None

    imprimir_separador()
    print("localidades disponibles en", municipio.nombre, ":")
    contador = 1
    for localidad in localidades:
        print(contador, "-", localidad.nombre)
        contador += 1
    imprimir_separador()

    try:
        opcion = int(input("selecciona el numero de la localidad: "))
    except ValueError:
        print("opcion invalida")
        return None, None

    if opcion < 1 or opcion > len(localidades):
        print("opcion invalida")
        return None, None

    localidad = localidades[opcion - 1]
    return municipio, localidad


def opcion_consultar_por_municipio(municipios, consultas):
    """flujo de consulta de clima seleccionando municipio y localidad"""
    municipio, localidad = seleccionar_localidad(municipios)
    if localidad is None:
        return

    temperatura = mostrar_clima(municipio, localidad)
    if temperatura is not None:
        consultas.append((municipio.nombre, localidad.nombre, temperatura))


def opcion_buscar_por_nombre(municipios, consultas):
    """flujo de busqueda de clima por nombre parcial de localidad"""
    texto = input("ingresa el nombre o parte del nombre de la localidad: ")
    coincidencias = buscar_localidad_por_nombre(municipios, texto)

    if len(coincidencias) == 0:
        print("no se encontraron localidades con ese nombre")
        return

    imprimir_separador()
    print("coincidencias encontradas:")
    contador = 1
    for municipio, localidad in coincidencias:
        print(contador, "-", localidad.nombre, "(" + municipio.nombre + ")")
        contador += 1
    imprimir_separador()

    try:
        opcion = int(input("selecciona el numero de la localidad: "))
    except ValueError:
        print("opcion invalida")
        return

    if opcion < 1 or opcion > len(coincidencias):
        print("opcion invalida")
        return

    municipio, localidad = coincidencias[opcion - 1]
    temperatura = mostrar_clima(municipio, localidad)
    if temperatura is not None:
        consultas.append((municipio.nombre, localidad.nombre, temperatura))


def normalizar_fecha(fecha_texto):
    """agrega ceros a la izquierda al mes y al dia si hacen falta, ej. 2025-1-1 a 2025-01-01"""
    partes = fecha_texto.split("-")
    anio = partes[0]
    mes = partes[1].zfill(2)
    dia = partes[2].zfill(2)
    return anio + "-" + mes + "-" + dia


def opcion_historico(municipios):
    """flujo de consulta de clima historico por periodo de una localidad"""
    municipio, localidad = seleccionar_localidad(municipios)
    if localidad is None:
        return

    fecha_inicio = input("ingresa la fecha de inicio (aaaa-mm-dd): ")
    fecha_fin = input("ingresa la fecha de fin (aaaa-mm-dd): ")

    try:
        fecha_inicio = normalizar_fecha(fecha_inicio)
        fecha_fin = normalizar_fecha(fecha_fin)
    except IndexError:
        print("formato de fecha invalido, usa aaaa-mm-dd")
        return

    print("consultando historico, esto puede tardar unos segundos...")
    try:
        tabla = consultar_historico(localidad.latitud, localidad.longitud, fecha_inicio, fecha_fin)
    except Exception:
        print("no se pudo consultar el historico, revisa las fechas e intenta de nuevo")
        return

    imprimir_separador()
    mensual = resumen_mensual(tabla)
    mostrar_resumen_mensual(mensual)

    promedio_temperatura, promedio_humedad, promedio_precipitacion, promedio_viento = promedios_generales(mensual)
    print("promedio general de temperatura:", round(promedio_temperatura, 2), "c")
    print("promedio general de humedad:", round(promedio_humedad, 2), "%")
    print("promedio general de precipitacion:", round(promedio_precipitacion, 2), "mm")
    print("promedio general de viento:", round(promedio_viento, 2), "km/h")
    imprimir_separador()

    anual = resumen_anual(tabla)
    año_mas_caluroso, año_mas_fresco, año_mas_lluvioso, año_mas_humedo = años_destacados(anual)
    print("año mas caluroso:", año_mas_caluroso)
    print("año mas fresco:", año_mas_fresco)
    print("año con mas precipitacion:", año_mas_lluvioso)
    print("año con mas humedad:", año_mas_humedo)
    imprimir_separador()

    graficar_evolucion_anual(anual)


def main():
    """funcion principal que ejecuta el sistema meteocaracas"""
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_datos = os.path.join(directorio_actual, "datos", "zonas_caracas.json")
    municipios = cargar_municipios(ruta_datos)
    mostrar_reporte_carga(municipios)

    consultas = []
    continuar = True

    while continuar:
        mostrar_menu()
        opcion = input("selecciona una opcion: ")

        if opcion == "1":
            opcion_consultar_por_municipio(municipios, consultas)
        elif opcion == "2":
            opcion_buscar_por_nombre(municipios, consultas)
        elif opcion == "3":
            mostrar_ranking_temperatura(consultas)
        elif opcion == "4":
            print("promedio general de la sesion:", round(promedio_general(consultas), 2), "c")
        elif opcion == "5":
            mostrar_cobertura_geografica(municipios)
        elif opcion == "6":
            opcion_historico(municipios)
        elif opcion == "0":
            print("gracias por usar meteocaracas")
            continuar = False
        else:
            print("opcion invalida, intenta de nuevo")

        print()


if __name__ == "__main__":
    main()
