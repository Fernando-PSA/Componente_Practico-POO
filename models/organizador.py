class Organizador:
    def __init__(self, id, cedula, nombre, correo, telefono, estado=True):
        self.id = id
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.estado = estado

    def convertir_a_diccionario(self):
        return {
            "id": self.id,
            "cedula": self.cedula,
            "nombre": self.nombre,
            "correo": self.correo,
            "telefono": self.telefono,
            "estado": self.estado
        }