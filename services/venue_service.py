from models.venue import Venue
from utils.generador_id import generar_id_secuencial
# Importamos las utilidades de validación correspondientes
from utils.validaciones import (
    pedir_solo_letras,
    pedir_alfanumerico,
    pedir_capacidad_venue,
    pedir_entero
)


class VenueService:

    def __init__(self, repo):
        self.repo = repo

    # =====================================================================
    # C - CREAR (Registrar Venue / Lugar)
    # =====================================================================
    def registrar(self):
        print("\n--- REGISTRAR VENUE (LUGAR) ---")
        
        # Delegamos el control de formato y obligatoriedad a validaciones.py
        nombre = pedir_solo_letras("Nombre del lugar (Venue): ")
        ciudad = pedir_solo_letras("Ciudad: ")
        direccion = pedir_alfanumerico("Dirección: ")
        capacidad_maxima = pedir_capacidad_venue("Capacidad máxima de aforo: ")

        # Listamos todos para generar el ID secuencial autoincremental desde 1
        venues_en_db = self.repo.listar("venues", solo_activos=False)

        # Instancia del modelo de dominio
        venue = Venue(
            generar_id_secuencial(venues_en_db),
            nombre,
            ciudad,
            direccion,
            capacidad_maxima,
            True
        )

        # Almacenamos en el archivo JSON
        self.repo.guardar("venues", venue.convertir_a_diccionario())
        print("[✔ ÉXITO] Venue registrado correctamente.")

    # =====================================================================
    # R - LEER (Listar Venues)
    # =====================================================================
    def listar(self):
        print("\n--- LISTADO DE VENUES (LUGARES) ---")
        venues = self.repo.listar("venues")

        if len(venues) == 0:
            print("[ℹ INFO] No existen venues registrados.")
            return

        for venue in venues:
            print(
                f"ID: {venue['id']} | "
                f"Nombre: {venue['nombre']} | "
                f"Ciudad: {venue['ciudad']} | "
                f"Dirección: {venue['direccion']} | "
                f"Capacidad_Maxima: {venue['capacidad_maxima']} personas"
            )

    # =====================================================================
    # U - ACTUALIZAR (Modificar Venue)
    # =====================================================================
    def modificar(self):
        print("\n--- MODIFICAR VENUE ---")
        id_venue = pedir_entero("Ingrese el ID del venue a modificar: ")
        venue = self.repo.buscar_por_id("venues", id_venue)

        if venue is None:
            print("[❌ ERROR] No existe un venue activo con ese ID.")
            return

        print("Deje vacío un campo si no desea modificarlo (Presione Enter).")

        # Al pasarle 'valor_actual', si presiona Enter se mantiene el valor original
        nuevo_nombre = pedir_solo_letras("Nombre nuevo", valor_actual=venue['nombre'])
        nueva_ciudad = pedir_solo_letras("Ciudad nueva", valor_actual=venue['ciudad'])
        nuevo_direccion = pedir_alfanumerico("Dirección nueva", valor_actual=venue['direccion'])
        nueva_capacidad = pedir_capacidad_venue("Capacidad nueva", valor_actual=venue['capacidad_maxima'])

        nuevos_datos = {
            "nombre": nuevo_nombre,
            "ciudad": nueva_ciudad,
            "direccion": nuevo_direccion,
            "capacidad_maxima": nueva_capacidad,
            "estado": True
        }

        self.repo.actualizar("venues", id_venue, nuevos_datos)
        print("[✔ ÉXITO] Venue modificado correctamente.")

    # =====================================================================
    # D - ELIMINAR (Eliminar Venue Lógico)
    # =====================================================================
    def eliminar(self):
        print("\n--- ELIMINAR VENUE ---")
        id_venue = pedir_entero("Ingrese el ID del venue a eliminar: ")

        eliminado = self.repo.eliminar_logico("venues", id_venue)

        if eliminado:
            print("[✔ ÉXITO] Venue eliminado lógicamente.")
        else:
            print("[❌ ERROR] No se encontró el venue o ya se encuentra inactivo.")