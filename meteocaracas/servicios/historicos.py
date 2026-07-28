"""modulo para consultar y analizar el clima historico de una localidad"""

import requests
import pandas as pd
import matplotlib.pyplot as plt


def consultar_historico(latitud, longitud, fecha_inicio, fecha_fin):
    """consulta el clima historico por hora entre dos fechas y retorna una tabla"""
    url = "https://archive-api.open-meteo.com/v1/archive"
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "start_date": fecha_inicio,
        "end_date": fecha_fin,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
    }

    respuesta = requests.get(url, params=parametros)
    datos = respuesta.json()
    horario = datos["hourly"]

    tabla = pd.DataFrame({
        "fecha": pd.to_datetime(horario["time"]),
        "temperatura": horario["temperature_2m"],
        "humedad": horario["relative_humidity_2m"],
        "precipitacion": horario["precipitation"],
        "viento": horario["wind_speed_10m"]
    })

    tabla["año"] = tabla["fecha"].dt.year
    tabla["mes"] = tabla["fecha"].dt.month

    return tabla


def resumen_mensual(tabla):
    """agrupa la tabla historica por año y mes y calcula los valores de cada magnitud"""
    resumen = tabla.groupby(["año", "mes"]).agg(
        temperatura=("temperatura", "mean"),
        humedad=("humedad", "mean"),
        precipitacion=("precipitacion", "sum"),
        viento=("viento", "mean")
    )
    resumen = resumen.reset_index()
    return resumen


def mostrar_resumen_mensual(resumen):
    """muestra en pantalla los valores mensuales de cada magnitud"""
    for fila in resumen.itertuples():
        print("año:", fila.año, "mes:", fila.mes)
        print("  temperatura promedio:", round(fila.temperatura, 2), "c")
        print("  humedad promedio:", round(fila.humedad, 2), "%")
        print("  precipitacion acumulada:", round(fila.precipitacion, 2), "mm")
        print("  viento promedio:", round(fila.viento, 2), "km/h")
        print()


def promedios_generales(resumen):
    """retorna el promedio de cada magnitud a partir del resumen mensual"""
    promedio_temperatura = resumen["temperatura"].mean()
    promedio_humedad = resumen["humedad"].mean()
    promedio_precipitacion = resumen["precipitacion"].mean()
    promedio_viento = resumen["viento"].mean()

    return promedio_temperatura, promedio_humedad, promedio_precipitacion, promedio_viento


def resumen_anual(tabla):
    """agrupa la tabla historica por año y calcula los valores de cada magnitud"""
    resumen = tabla.groupby("año").agg(
        temperatura=("temperatura", "mean"),
        humedad=("humedad", "mean"),
        precipitacion=("precipitacion", "sum"),
        viento=("viento", "mean")
    )
    resumen = resumen.reset_index()
    return resumen


def años_destacados(resumen_por_año):
    """retorna el año mas caluroso, mas fresco, mas lluvioso y mas humedo"""
    fila_mas_calurosa = resumen_por_año.loc[resumen_por_año["temperatura"].idxmax()]
    fila_mas_fresca = resumen_por_año.loc[resumen_por_año["temperatura"].idxmin()]
    fila_mas_lluviosa = resumen_por_año.loc[resumen_por_año["precipitacion"].idxmax()]
    fila_mas_humeda = resumen_por_año.loc[resumen_por_año["humedad"].idxmax()]

    año_mas_caluroso = int(fila_mas_calurosa["año"])
    año_mas_fresco = int(fila_mas_fresca["año"])
    año_mas_lluvioso = int(fila_mas_lluviosa["año"])
    año_mas_humedo = int(fila_mas_humeda["año"])

    return año_mas_caluroso, año_mas_fresco, año_mas_lluvioso, año_mas_humedo


def graficar_evolucion_anual(resumen_por_año):
    """muestra un grafico con la evolucion de cada magnitud por año"""
    figura, graficos = plt.subplots(2, 2, figsize=(10, 8))

    graficos[0, 0].plot(resumen_por_año["año"], resumen_por_año["temperatura"], marker="o")
    graficos[0, 0].set_title("temperatura promedio por año")

    graficos[0, 1].plot(resumen_por_año["año"], resumen_por_año["humedad"], marker="o")
    graficos[0, 1].set_title("humedad promedio por año")

    graficos[1, 0].plot(resumen_por_año["año"], resumen_por_año["precipitacion"], marker="o")
    graficos[1, 0].set_title("precipitacion acumulada por año")

    graficos[1, 1].plot(resumen_por_año["año"], resumen_por_año["viento"], marker="o")
    graficos[1, 1].set_title("viento promedio por año")

    plt.tight_layout()
    plt.show()
