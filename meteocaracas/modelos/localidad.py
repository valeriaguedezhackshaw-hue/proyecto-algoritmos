"""clase que representa una localidad de un municipio"""


class Localidad:
    """representa una localidad con su nombre y coordenadas geograficas"""

    def __init__(self, nombre, latitud, longitud):
        """inicializa la localidad con nombre y coordenadas opcionales"""
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    def tiene_coordenadas(self):
        """retorna true si la localidad tiene coordenadas validas"""
        return self.latitud is not None and self.longitud is not None

    def __str__(self):
        """retorna una representacion legible de la localidad"""
        return self.nombre
