"""modulo para generar estadisticas y reportes del sistema"""


def ranking_temperatura(consultas):
    """retorna la consulta mas calida y la mas fria de la lista de consultas"""
    if len(consultas) == 0:
        return None, None

    mas_calida = consultas[0]
    mas_fria = consultas[0]

    for consulta in consultas:
        temperatura = consulta[2]
        if temperatura > mas_calida[2]:
            mas_calida = consulta
        if temperatura < mas_fria[2]:
            mas_fria = consulta

    return mas_calida, mas_fria


def mostrar_ranking_temperatura(consultas):
    """muestra en pantalla la localidad mas calida y la mas fria consultadas"""
    mas_calida, mas_fria = ranking_temperatura(consultas)

    if mas_calida is None:
        print("aun no se han realizado consultas en esta sesion")
        return

    print("localidad mas calida:", mas_calida[1], "(" + mas_calida[0] + ")", "-", mas_calida[2], "c")
    print("localidad mas fria:", mas_fria[1], "(" + mas_fria[0] + ")", "-", mas_fria[2], "c")


def promedio_general(consultas):
    """retorna el promedio de temperatura de las consultas realizadas"""
    if len(consultas) == 0:
        return 0

    suma = 0
    for consulta in consultas:
        suma = suma + consulta[2]

    return suma / len(consultas)


def cobertura_geografica(municipios):
    """retorna una lista con el municipio y sus localidades sin coordenadas"""
    cobertura = []
    for municipio in municipios:
        localidades_sin_coordenadas = []
        for localidad in municipio.localidades:
            if not localidad.tiene_coordenadas():
                localidades_sin_coordenadas.append(localidad)
        cobertura.append((municipio.nombre, localidades_sin_coordenadas))
    return cobertura


def mostrar_cobertura_geografica(municipios):
    """muestra en pantalla las localidades sin coordenadas agrupadas por municipio"""
    cobertura = cobertura_geografica(municipios)
    for nombre_municipio, localidades_sin_coordenadas in cobertura:
        print("municipio:", nombre_municipio)
        if len(localidades_sin_coordenadas) == 0:
            print("  todas las localidades tienen coordenadas")
        else:
            for localidad in localidades_sin_coordenadas:
                print("  -", localidad.nombre)
        print()
