class Organizador:
    def __init__(self, id, cedula, nombres, apellidos, correo, telefono, estado=True):
        self.id = id
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.telefono = telefono
        self.estado = estado

    def convertir_a_diccionario(self):
        return {
            "id": self.id,
            "cedula": self.cedula,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "correo": self.correo,
            "telefono": self.telefono,
            "estado": self.estado
        }