"""modulo para buscar localidades por nombre"""


def listar_localidades_con_coordenadas(municipio):
    """retorna la lista de localidades del municipio que tienen coordenadas validas"""
    localidades_validas = []
    for localidad in municipio.localidades:
        if localidad.tiene_coordenadas():
            localidades_validas.append(localidad)
    return localidades_validas


def buscar_localidad_por_nombre(municipios, texto):
    """busca en todos los municipios localidades con coordenadas cuyo nombre contenga el texto"""
    coincidencias = []
    texto_buscado = texto.lower()
    for municipio in municipios:
        for localidad in municipio.localidades:
            if localidad.tiene_coordenadas() and texto_buscado in localidad.nombre.lower():
                coincidencias.append((municipio, localidad))
    return coincidencias
