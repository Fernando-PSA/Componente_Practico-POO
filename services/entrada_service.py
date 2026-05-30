from models.entrada import Entrada
from utils.generador_id import generar_id_secuencial
from utils.validaciones import pedir_entero, validar_codigo_unico, pedir_entero_positivo


class EntradaService:

    # Constructor de la clase
    def __init__(self, repo):
        self.repo = repo

    # Metodo para emitir entradas
    def registrar(self):
        print("\n--- EMITIR ENTRADA ---")

        # ==============================
        # LISTAR EVENTOS
        # ==============================

        eventos = self.repo.listar("eventos")

        if len(eventos) == 0:
            print("No existen eventos registrados.")
            return

        print("\n--- EVENTOS DISPONIBLES ---")

        for evento in eventos:
            print(
                f"ID: {evento['id']} | "
                f"Nombre: {evento['nombre']} | "
                f"Ciudad: {evento['ciudad']} | "
                f"Fecha: {evento['fecha']} | "
                f"Capacidad Máxima: {evento['capacidad_maxima']}"
            )

        evento_id = pedir_entero("Seleccione el ID del evento: ")

        evento = self.repo.buscar_por_id("eventos", entrada.get("evento_id"))

        if evento is None or evento["estado"] is False:
            print("El evento no existe o está inactivo.")
            return

        # ==============================
        # CONTROL DE CAPACIDAD MAXIMA
        # ==============================

        entradas = self.repo.listar("entradas")

        entradas_vendidas = sum(1 for entrada in entradas if entrada["evento_id"] == evento_id and entrada["estado"])

        if entradas_vendidas >= evento["capacidad_maxima"]:
            print("No existen cupos disponibles para este evento.")
            return

        # ==============================
        # LISTAR ASISTENTES
        # ==============================

        asistentes = self.repo.listar("asistentes")

        if len(asistentes) == 0:
            print("No existen asistentes registrados.")
            return

        print("\n--- ASISTENTES DISPONIBLES ---")

        for asistente in asistentes:
            print(
                f"ID: {asistente['id']} | "
                f"Nombres: {asistente['nombres']} {asistente['apellidos']} | "
                f"Cédula: {asistente['cedula']}"
            )

        while True:
            asistente_id = pedir_entero("Seleccione el ID del asistente: ")

            asistente = self.repo.buscar_por_id("asistentes", asistente_id)

            if asistente is None:
                print("Error. El asistente no existe.")
                continue

            break

        # ==============================
        # DATOS DE LA ENTRADA
        # ==============================
        while True:
            codigo = pedir_entero_positivo("Código de entrada: ")

            if not validar_codigo_unico(
                self.repo,
                "entradas",
                "codigo",
                codigo
            ):

                print("Error. Ya existe una entrada con ese código.")
                continue

            break


        # ==============================
        # VALIDAR PRECIO
        # ==============================
        precio = pedir_entero_positivo("Precio de la entrada: ")

        entradas = self.repo.listar("entradas", solo_activos=False)

        # Crear objeto Entrada
        entrada = Entrada(
            generar_id_secuencial(entradas),
            codigo,
            evento_id,
            asistente_id,
            precio,
            True
        )

        # Guardar entrada
        self.repo.guardar("entradas", entrada.convertir_a_diccionario())

        print("Entrada emitida correctamente.")

    # Metodo para listar entradas
    def listar(self):
        print("\n--- LISTADO DE ENTRADAS ---")

        entradas = self.repo.listar("entradas")

        if not entradas:
            print("No existen entradas registradas.")
            return

        for entrada in entradas:

            evento = self.repo.buscar_por_id("eventos", entrada["evento_id"])

            asistente = self.repo.buscar_por_id("asistentes", entrada["asistente_id"])

            nombre_evento = (evento["nombre"] if evento else "No encontrado")

            nombre_asistente = (f"{asistente['nombres']} {asistente['apellidos']}" if asistente else "No encontrado")

            print(
                f"ID Entrada: {entrada['id']} | "
                f"Código: {entrada['codigo']} | "
                f"Evento: {nombre_evento} | "
                f"Asistente: {nombre_asistente} | "
                f"Precio: ${entrada['precio']}"
            )

    # Metodo para cancelar entradas
    def eliminar(self):
        print("\n--- CANCELAR ENTRADA ---")

        id_entrada = pedir_entero("Ingrese el ID de la entrada a cancelar: ")

        eliminado = self.repo.eliminar_logico("entradas", id_entrada)

        if eliminado:
            print("Entrada cancelada correctamente.")
        else:
            print("No se encontró la entrada.")
            
            
    def listar_asistentes_ordenada(self):
        print("\n--- LISTA DE ASISTENTES ORDENADA ---")

        entradas = self.repo.listar("entradas")
        asistentes = self.repo.listar("asistentes")

        if not entradas or not asistentes:
            print("No hay datos suficientes.")
            return

        print("\nOrdenar por:")
        print("1. Apellido")
        print("2. Código de entrada")

        opcion = pedir_entero("Seleccione opción: ")

        lista = []

        for entrada in entradas:
            asistente = self.repo.buscar_por_id("asistentes", entrada["asistente_id"])

            if asistente:
                lista.append({
                    "apellido": asistente["apellidos"],
                    "nombre": asistente["nombres"],
                    "codigo": entrada["codigo"],
                    "evento_id": entrada["evento_id"]
                })

        if opcion == 1:
            lista.sort(key=lambda x: x["apellido"].lower())

        elif opcion == 2:
            lista.sort(key=lambda x: x["codigo"])

        else:
            print("Opción inválida.")
            return

        for item in lista:
            print(
                f"Apellido: {item['apellido']} | "
                f"Nombre: {item['nombre']} | "
                f"Código Entrada: {item['codigo']}"
            )