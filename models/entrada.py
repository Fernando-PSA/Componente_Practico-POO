class Entrada:
    def __init__(self, id, codigo, evento_id, asistente_id, precio, estado=True):
        self.id = id
        self.codigo = codigo
        self.evento_id = evento_id
        self.asistente_id = asistente_id
        self.precio = precio
        self.estado = estado

    def convertir_a_diccionario(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "evento_id": self.evento_id,
            "asistente_id": self.asistente_id,
            "precio": self.precio,
            "estado": self.estado
        }