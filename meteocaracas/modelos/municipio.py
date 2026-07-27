"""clase que representa un municipio y sus localidades"""


class Municipio:
    """representa un municipio y la lista de sus localidades"""

    def __init__(self, nombre):
        """inicializa el municipio con nombre y lista vacia de localidades"""
        self.nombre = nombre
        self.localidades = []

    def agregar_localidad(self, localidad):
        """agrega una localidad a la lista del municipio"""
        self.localidades.append(localidad)

    def contar_localidades(self):
        """retorna la cantidad total de localidades del municipio"""
        return len(self.localidades)

    def contar_con_coordenadas(self):
        """retorna la cantidad de localidades con coordenadas validas"""
        contador = 0
        for localidad in self.localidades:
            if localidad.tiene_coordenadas():
                contador += 1
        return contador

    def contar_sin_coordenadas(self):
        """retorna la cantidad de localidades sin coordenadas validas"""
        return self.contar_localidades() - self.contar_con_coordenadas()

    def porcentaje_con_coordenadas(self):
        """retorna el porcentaje de localidades con coordenadas validas"""
        total = self.contar_localidades()
        if total == 0:
            return 0
        return (self.contar_con_coordenadas() / total) * 100

    def __str__(self):
        """retorna una representacion legible del municipio"""
        return self.nombre
