class Venue:
    def __init__(self, id, nombre, ciudad, direccion, capacidad_maxima, estado=True):
        self.id = id
        self.nombre = nombre
        self.ciudad = ciudad
        self.direccion = direccion
        self.capacidad_maxima = capacidad_maxima
        self.estado = estado

    def convertir_a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ciudad": self.ciudad,
            "direccion": self.direccion,
            "capacidad_maxima": self.capacidad_maxima,
            "estado": self.estado
        }