class Evento:
    def __init__(self, id, nombre, ciudad, fecha, capacidad_maxima, organizador_id, venue_id, patrocinadores_ids,estado=True):
        self.id = id
        self.nombre = nombre
        self.ciudad = ciudad
        self.fecha = fecha
        self.capacidad_maxima = capacidad_maxima
        self.organizador_id = organizador_id
        self.venue_id = venue_id
        self.patrocinadores_ids = patrocinadores_ids
        self.estado = estado

    def convertir_a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ciudad": self.ciudad,
            "fecha": self.fecha,
            "capacidad_maxima": self.capacidad_maxima,
            "organizador_id": self.organizador_id,
            "venue_id": self.venue_id,
            "patrocinadores_ids": self.patrocinadores_ids,
            "estado": self.estado
        }
        
# organizador_id y venue_id se utilizan para crear relaciones entre las entidades del sistema.
# En lugar de guardar toda la información del organizador y del lugar dentro del evento,
# únicamente se almacena el ID de cada uno para evitar duplicar datos y mantener una mejor organización.
# Posteriormente, mediante los métodos del repository y services, es posible acceder a la información completa
# del organizador o del venue utilizando esos IDs. Este funcionamiento es similar a las relaciones que se
# manejan en bases de datos reales mediante claves foráneas (Foreign Keys).