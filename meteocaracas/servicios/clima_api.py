"""modulo para consultar el clima en tiempo real con la api de open-meteo"""

import requests

from modelos.clima import Clima


def consultar_clima_actual(latitud, longitud):
    """consulta el clima actual de una coordenada y retorna un objeto clima"""
    url = "https://api.open-meteo.com/v1/forecast"
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    }

    respuesta = requests.get(url, params=parametros)
    datos = respuesta.json()
    actual = datos["current"]

    temperatura = actual["temperature_2m"]
    humedad = actual["relative_humidity_2m"]
    viento = actual["wind_speed_10m"]
    estado_tiempo = obtener_estado_tiempo(actual["weather_code"])

    return Clima(temperatura, humedad, viento, estado_tiempo)


def obtener_estado_tiempo(codigo):
    """traduce el codigo del clima de la api a un texto legible"""
    if codigo == 0:
        return "Despejado"
    elif codigo == 1 or codigo == 2 or codigo == 3:
        return "Parcialmente nublado"
    elif codigo == 45 or codigo == 48:
        return "Niebla"
    elif codigo == 51 or codigo == 53 or codigo == 55:
        return "Llovizna"
    elif codigo == 56 or codigo == 57:
        return "Llovizna helada"
    elif codigo == 61 or codigo == 63 or codigo == 65:
        return "Lluvia"
    elif codigo == 66 or codigo == 67:
        return "Lluvia helada"
    elif codigo == 71 or codigo == 73 or codigo == 75:
        return "Nieve"
    elif codigo == 77:
        return "Granizo de nieve"
    elif codigo == 80 or codigo == 81 or codigo == 82:
        return "Chubascos de lluvia"
    elif codigo == 85 or codigo == 86:
        return "Chubascos de nieve"
    elif codigo == 95 or codigo == 96 or codigo == 99:
        return "Tormenta electrica"
    else:
        return "Estado del tiempo desconocido"
