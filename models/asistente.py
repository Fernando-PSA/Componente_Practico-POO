class Asistente:
    def __init__(self, id, cedula, nombres, apellidos, correo, direccion, estado=True):
        self.id = id
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.direccion = direccion
        self.estado = estado

    def convertir_a_diccionario(self):
        
        return {
            "id": self.id,
            "cedula": self.cedula,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "correo": self.correo,
            "direccion": self.direccion,
            "estado": self.estado
        }