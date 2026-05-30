class Patrocinador:
    def __init__(self, id, empresa, telefono, aporte, estado=True):
        self.id = id
        self.empresa = empresa
        self.telefono = telefono
        self.aporte = aporte
        self.estado = estado

    def convertir_a_diccionario(self):
        return {
            "id": self.id,
            "empresa": self.empresa,
            "telefono": self.telefono,
            "aporte": self.aporte,
            "estado": self.estado
        }