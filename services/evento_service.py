import re

from models.evento import Evento
from utils.generador_id import generar_id_secuencial
from utils.validaciones import pedir_solo_letras, pedir_fecha, pedir_entero, validar_fecha


class EventoService:

    # Constructor de la clase
    def __init__(self, repo):
        self.repo = repo

    # Metodo para registrar eventos
    def registrar(self):
        print("\n--- REGISTRAR EVENTO ---")

        while True:
            nombre = pedir_solo_letras("Nombre del evento: ")

            existente = self.repo.buscar_por_campo(
                "eventos",
                "nombre",
                nombre
            )

            if existente:
                print("Ya existe un evento con ese nombre.")
                continue

            break
        
        ciudad = pedir_solo_letras("Ciudad: ")
        fecha = pedir_fecha("Fecha del evento: ")

        # ==============================
        # LISTAR ORGANIZADORES
        # ==============================

        organizadores = self.repo.listar("organizadores")

        if len(organizadores) == 0:
            print("No existen organizadores registrados.")
            return

        print("\n--- ORGANIZADORES DISPONIBLES ---")

        for organizador in organizadores:
            print(
                f"ID: {organizador['id']} | "
                f"Nombre: {organizador['nombre']} | "
                f"Correo: {organizador['correo']} | "
                f"Teléfono: {organizador['telefono']}"
            )

        while True:
            organizador_id = pedir_entero("Seleccione el ID del organizador: ")

            organizador = self.repo.buscar_por_id("organizadores", organizador_id)

            if organizador is None:
                print("Error. El organizador no existe.")
                continue

            break

        # ==============================
        # LISTAR VENUES
        # ==============================
        venues = self.repo.listar("venues")

        if len(venues) == 0:
            print("No existen venues registrados.")
            return

        print("\n--- VENUES DISPONIBLES ---")

        for venue in venues:
            print(
                f"ID: {venue['id']} | "
                f"Nombre: {venue['nombre']} | "
                f"Ciudad: {venue['ciudad']} | "
                f"Capacidad Máxima: {venue['capacidad_maxima']}"
            )

        while True:
            venue_id = pedir_entero("Seleccione el ID del venue: ")

            venue = self.repo.buscar_por_id("venues", venue_id)

            if venue is None:
                print("Error. El venue no existe.")
                continue

            if venue["ciudad"].lower() != ciudad.lower():
                print("No se pudo registrar el evento porque el venue no pertenece a la misma ciudad.")
                print("Regresando al menú de eventos...")
                return

            break
        
        # ==============================
        # LISTAR PATROCINADORES
        # ==============================
        patrocinadores = self.repo.listar("patrocinadores")

        patrocinadores_ids = []

        if len(patrocinadores) > 0:

            print("\n--- PATROCINADORES DISPONIBLES ---")

            for patrocinador in patrocinadores:
                print(
                    f"ID: {patrocinador['id']} | "
                    f"Empresa: {patrocinador['empresa']} | "
                    f"Aporte: ${patrocinador['aporte']}"
                )

            ids = input("Ingrese IDs de patrocinadores separados por coma (Enter para ninguno): ").strip()

            if ids != "":
                lista_ids = ids.split(",")

                for id_texto in lista_ids:
                    
                    if id_texto.strip() == "":
                        continue
                    
                    try:
                        id_pat = int(id_texto.strip())

                        patrocinador = self.repo.buscar_por_id("patrocinadores", id_pat)

                        if patrocinador:

                            if id_pat not in patrocinadores_ids:
                                patrocinadores_ids.append(id_pat)

                            else:
                                print(f"El patrocinador ID {id_pat} ya fue agregado.")
                                
                        else:
                            print(f"Patrocinador con ID {id_pat} no existe.")

                    except ValueError:
                        print(f"'{id_texto.strip()}' no es un ID válido.")
                        
        if len(patrocinadores_ids) == 0:
            print("Debe seleccionar al menos un patrocinador.")
            
            return
        
        # La capacidad maxima del evento sera igual
        # a la capacidad maxima del venue seleccionado
        capacidad_maxima = venue["capacidad_maxima"]

        # Obtener eventos registrados
        eventos = self.repo.listar("eventos", solo_activos=False)

        # Crear objeto Evento
        evento = Evento(
            generar_id_secuencial(eventos),
            nombre,
            ciudad,
            fecha,
            capacidad_maxima,
            organizador_id,
            venue_id,
            patrocinadores_ids,
            True
        )

        # Guardar evento
        self.repo.guardar("eventos", evento.convertir_a_diccionario())
        print("Evento registrado correctamente.")

    # Metodo para listar eventos
    def listar(self):
        print("\n--- LISTADO DE EVENTOS ---")

        eventos = self.repo.listar("eventos")

        if len(eventos) == 0:
            print("No existen eventos registrados.")
            return

        for evento in eventos:

            organizador = self.repo.buscar_por_id("organizadores", evento["organizador_id"])

            venue = self.repo.buscar_por_id("venues", evento["venue_id"])

            nombre_organizador = (organizador["nombre"] if organizador else "No encontrado")

            nombre_venue = (venue["nombre"] if venue else "No encontrado")

            patrocinadores_texto = "Ninguno"

            if len(evento.get("patrocinadores_ids", [])) > 0:

                empresas = []

                for id_pat in evento.get("patrocinadores_ids", []):

                    patrocinador = self.repo.buscar_por_id("patrocinadores", id_pat)

                    if patrocinador:
                        empresas.append(patrocinador["empresa"])

                patrocinadores_texto = ", ".join(empresas)

            print(
                f"ID Evento: {evento['id']} | "
                f"Nombre: {evento['nombre']} | "
                f"Ciudad: {evento['ciudad']} | "
                f"Fecha: {evento['fecha']} | "
                f"Capacidad Máxima: {evento['capacidad_maxima']} | "
                f"Organizador: {nombre_organizador} | "
                f"Venue: {nombre_venue} | "
                f"Patrocinadores: {patrocinadores_texto}"
            )

    # Metodo para modificar eventos
    def modificar(self):
        print("\n--- MODIFICAR EVENTO ---")

        while True:
            id_evento = pedir_entero("Ingrese el ID del evento a modificar: ")

            evento = self.repo.buscar_por_id("eventos", id_evento)

            if evento is None:
                print("Error. No existe un evento activo con ese ID.")
                continue

            break

        print("Deje vacío un campo si no desea modificarlo.")

        while True:
            nuevo_nombre = input(f"Nombre actual ({evento['nombre']}): ").strip()

            if nuevo_nombre == "":
                nuevo_nombre = evento["nombre"]
                break

            if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+", nuevo_nombre):
                print("Error. El nombre solo permite letras.")
                continue
            
            existente = self.repo.buscar_por_campo("eventos", "nombre", nuevo_nombre)

            if existente and existente["id"] != id_evento:
                print("Ya existe un evento con ese nombre.")
                continue

            break

        while True:
            nueva_ciudad = input(f"Ciudad actual ({evento['ciudad']}): ").strip()

            if nueva_ciudad == "":
                nueva_ciudad = evento["ciudad"]
                break

            if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+", nueva_ciudad):
                print("Error. La ciudad solo permite letras.")
                continue

            break

        while True:
            nueva_fecha = input(f"Fecha actual ({evento['fecha']}): ").strip()

            if nueva_fecha == "":
                nueva_fecha = evento["fecha"]
                break

            if validar_fecha(nueva_fecha):
                break

            print("Error. La fecha no es válida, use dd/mm/yyyy o dd-mm-yyyy.")

        venue = self.repo.buscar_por_id("venues", evento["venue_id"])

        if venue["ciudad"].lower() != nueva_ciudad.lower():
            print("Error. La ciudad del evento debe coincidir con la ciudad del venue asignado.")
            return

        nuevos_datos = {
            "nombre": nuevo_nombre,
            "ciudad": nueva_ciudad,
            "fecha": nueva_fecha,
            "estado": True
        }

        self.repo.actualizar(
            "eventos",
            id_evento,
            nuevos_datos
        )

        print("Evento modificado correctamente.")

    # Metodo para eliminar eventos
    def eliminar(self):
        print("\n--- ELIMINAR EVENTO ---")

        id_evento = pedir_entero("Ingrese el ID del evento a eliminar: ")

        entradas = self.repo.listar("entradas")

        for entrada in entradas:

            if entrada["evento_id"] == id_evento:
                print("No puede eliminar el evento porque tiene entradas asociadas.")
                return

        eliminado = self.repo.eliminar_logico("eventos", id_evento)

        if eliminado:
            print("Evento eliminado lógicamente.")
        else:
            print("No se encontró el evento.")
       
            
    def ingresos_por_evento(self):
        print("\n--- INGRESOS POR EVENTO ---")

        eventos = self.repo.listar("eventos")

        if not eventos:
            print("No hay eventos.")
            return

        for evento in eventos:

            entradas = self.repo.listar("entradas")

            total_entradas = sum(entrada["precio"] for entrada in entradas if entrada["evento_id"] == evento["id"] and entrada["estado"])

            patrocinio_total = 0

            for id_pat in evento.get("patrocinadores_ids", []):

                patrocinador = self.repo.buscar_por_id("patrocinadores", id_pat)

                if patrocinador:
                    patrocinio_total += patrocinador["aporte"]

            total = total_entradas + patrocinio_total

            print(
                f"Evento: {evento['nombre']} | "
                f"Ingresos entradas: ${total_entradas} | "
                f"Patrocinios: ${patrocinio_total} | "
                f"TOTAL: ${total}"
            )
            
            
    def filtrar_eventos(self):
        print("\n--- FILTRAR EVENTOS ---")

        print("1. Por ciudad")
        print("2. Por rango de fechas")

        opcion = pedir_entero("Seleccione opción: ")

        eventos = self.repo.listar("eventos")

        if not eventos:
            print("No hay eventos.")
            return

        if opcion == 1:

            ciudad = pedir_solo_letras("Ingrese ciudad: ")

            filtrados = [e for e in eventos if e["ciudad"].lower() == ciudad.lower()]

        elif opcion == 2:

            fecha_inicio = pedir_fecha("Fecha inicio: ")
            fecha_fin = pedir_fecha("Fecha fin: ")

            filtrados = [e for e in eventos if fecha_inicio <= e["fecha"] <= fecha_fin]

        else:
            print("Opción inválida.")
            return

        if not filtrados:
            print("No se encontraron eventos.")
            return

        for e in filtrados:
            print(
                f"ID: {e['id']} | "
                f"Nombre: {e['nombre']} | "
                f"Ciudad: {e['ciudad']} | "
                f"Fecha: {e['fecha']}"
            )