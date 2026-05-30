import re

from models.venue import Venue
from utils.generador_id import generar_id_secuencial
from utils.validaciones import pedir_alfanumerico, pedir_solo_letras, pedir_entero_positivo, pedir_entero


class VenueService:

    # Constructor de la clase
    def __init__(self, repo):
        self.repo = repo

    # Metodo para registrar un venue
    def registrar(self):
        print("\n--- REGISTRAR VENUE ---")

        while True:
            nombre = pedir_alfanumerico("Nombre del venue: ")

            existente = self.repo.buscar_por_campo(
                "venues",
                "nombre",
                nombre
            )

            if existente:
                print("Ya existe un venue con ese nombre.")
                continue

            break
        
        ciudad = pedir_solo_letras("Ciudad: ")
        direccion = pedir_alfanumerico("Dirección: ")
        capacidad_maxima = pedir_entero_positivo("Capacidad máxima: ")

        # Obtener todos los venues
        venues = self.repo.listar("venues", solo_activos=False)

        # Crear objeto Venue
        venue = Venue(
            generar_id_secuencial(venues),
            nombre,
            ciudad,
            direccion,
            capacidad_maxima,
            True
        )

        # Guardar venue en formato diccionario
        self.repo.guardar("venues", venue.convertir_a_diccionario())

        print("Venue registrado correctamente.")

    # Metodo para listar venues
    def listar(self):
        print("\n--- LISTADO DE VENUES ---")

        venues = self.repo.listar("venues")

        if len(venues) == 0:
            print("No existen venues registrados.")
            return

        for venue in venues:
            print(
                f"ID: {venue['id']} | "
                f"Nombre: {venue['nombre']} | "
                f"Ciudad: {venue['ciudad']} | "
                f"Dirección: {venue['direccion']} | "
                f"Capacidad Máxima: {venue['capacidad_maxima']}"
            )

    # Metodo para modificar venues
    def modificar(self):
        print("\n--- MODIFICAR VENUE ---")

        while True:
            id_venue = pedir_entero("Ingrese el ID del venue a modificar: ")

            venue = self.repo.buscar_por_id("venues", id_venue)

            if venue is None:
                print("Error. No existe un venue activo con ese ID.")
                continue

            break

        print("Deje vacío un campo si no desea modificarlo.")

        while True:
            nuevo_nombre = input(f"Nombre actual ({venue['nombre']}): ").strip()

            if nuevo_nombre == "":
                nuevo_nombre = venue["nombre"]
                break

            if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9 ]+", nuevo_nombre):
                print("Error. El nombre solo puede contener letras y números.")
                continue
            
            existente = self.repo.buscar_por_campo(
                "venues",
                "nombre",
                nuevo_nombre
            )

            if existente and existente["id"] != id_venue:
                print("Ya existe un venue con ese nombre.")
                continue

            if nuevo_nombre.isdigit():
                print("Error. El nombre no puede contener solo números.")
                continue

            break

        while True:
            nueva_ciudad = input(f"Ciudad actual ({venue['ciudad']}): ").strip()

            if nueva_ciudad == "":
                nueva_ciudad = venue["ciudad"]
                break

            if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+", nueva_ciudad):
                print("Error. La ciudad solo puede contener letras.")
                continue

            break

        while True:
            nueva_direccion = input(f"Dirección actual ({venue['direccion']}): ").strip()

            if nueva_direccion == "":
                nueva_direccion = venue["direccion"]
                break

            if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9 ]+", nueva_direccion):
                print("Error. La dirección solo puede contener letras y números.")
                continue

            if nueva_direccion.isdigit():
                print("Error. La dirección no puede contener solo números.")
                continue

            break

        while True:
            nueva_capacidad = input(f"Capacidad máxima actual ({venue['capacidad_maxima']}): ").strip()

            if nueva_capacidad == "":
                nueva_capacidad = venue["capacidad_maxima"]
                break

            if not nueva_capacidad.isdigit():
                print("Error. La capacidad máxima solo permite números enteros.")
                continue

            nueva_capacidad = int(nueva_capacidad)

            if nueva_capacidad <= 0:
                print("Error. La capacidad máxima debe ser mayor a 0.")
                continue

            break

        nuevos_datos = {
            "nombre": nuevo_nombre,
            "ciudad": nueva_ciudad,
            "direccion": nueva_direccion,
            "capacidad_maxima": nueva_capacidad,
            "estado": True
        }

        self.repo.actualizar(
            "venues",
            id_venue,
            nuevos_datos
        )

        print("Venue modificado correctamente.")

    # Metodo para eliminar venues
    def eliminar(self):
        print("\n--- ELIMINAR VENUE ---")

        id_venue = pedir_entero("Ingrese el ID del venue a eliminar: ")

        eventos = self.repo.listar("eventos")

        for evento in eventos:
            if evento["venue_id"] == id_venue:
                print("No puede eliminar el venue porque está asignado a un evento.")
                return

        eliminado = self.repo.eliminar_logico("venues", id_venue)

        if eliminado:
            print("Venue eliminado lógicamente.")
        else:
            print("No se encontró el venue.")