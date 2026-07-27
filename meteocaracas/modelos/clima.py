"""clase que representa el clima consultado para una localidad"""


class Clima:
    """representa los datos meteorologicos obtenidos de la api"""

    def __init__(self, temperatura, humedad, viento, estado_tiempo):
        """inicializa el clima con temperatura, humedad, viento y estado"""
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.estado_tiempo = estado_tiempo

    def __str__(self):
        """retorna una representacion legible del clima"""
        return "{}c, humedad {}%, viento {}km/h, {}".format(
            self.temperatura, self.humedad, self.viento, self.estado_tiempo
        )
