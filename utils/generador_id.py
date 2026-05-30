def generar_id_secuencial(registros):
    if len(registros) == 0:
        return 1

    ultimo_id = max(registro["id"] for registro in registros)
    return ultimo_id + 1