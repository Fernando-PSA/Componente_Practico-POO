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
        
        # [L-07] Unicidad de nombre del venue (case-insensitive) para evitar duplicados confusos en la selección
        while True:
            nombre = pedir_solo_letras("Nombre del lugar (Venue)")
            venues_activos = self.repo.listar("venues")
            duplicado = next((v for v in venues_activos if v["nombre"].lower() == nombre.lower()), None)
            if duplicado:
                print(f"[❌ ERROR] Ya existe un venue registrado con el nombre '{nombre}'. Ingrese uno diferente.")
                continue
            break

        ciudad = pedir_solo_letras("Ciudad")
        direccion = pedir_alfanumerico("Dirección")
        capacidad_maxima = pedir_capacidad_venue("Capacidad máxima de aforo")

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
    # U - ACTUALIZAR (Modificar Venue - VERSIÓN CON REINTENTOS)
    # =====================================================================
    def modificar(self):
        print("\n--- MODIFICAR VENUE ---")
        
        # 🔄 BUCLE 1: Reintenta de forma interactiva si el ID del local no existe
        while True:
            id_venue = pedir_entero("Ingrese el ID del venue a modificar o 0 para cancelar")

            if id_venue == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            venue = self.repo.buscar_por_id("venues", id_venue)

            if venue is None:
                print(f"[❌ ERROR] No existe un venue activo con el ID {id_venue}.")
                print("Por favor, verifique e intente con un ID válido de la lista.\n")
                continue # 🔄 Se mantiene en el bucle solicitando el ID otra vez
                
            break  # 🏁 Si el ID es correcto, rompe el ciclo para editar los campos

        print("Deje vacío un campo si no desea modificarlo (Presione Enter).")

        # Al pasarle 'valor_actual', si presiona Enter se mantiene el valor original
        nuevo_nombre = pedir_solo_letras("Nombre nuevo", valor_actual=venue['nombre'])
        nueva_ciudad = pedir_solo_letras("Ciudad nueva", valor_actual=venue['ciudad'])
        nuevo_direccion = pedir_alfanumerico("Dirección nueva", valor_actual=venue['direccion'])
        nueva_capacidad = pedir_capacidad_venue("Capacidad nueva", valor_actual=venue['capacidad_maxima'])

        # [L-02] Bloquea el cambio de ciudad si el venue ya tiene eventos activos asignados,
        #         para no romper la regla de negocio "venue y evento deben ser de la misma ciudad"
        if nueva_ciudad.lower() != venue["ciudad"].lower():
            eventos_del_venue = [e for e in self.repo.listar("eventos") if e["venue_id"] == id_venue]
            if eventos_del_venue:
                print(f"[❌ ERROR] No se puede cambiar la ciudad: este venue tiene {len(eventos_del_venue)} evento(s) activo(s) asignado(s).")
                print("[ℹ INFO] Elimine primero los eventos vinculados antes de cambiar la ciudad del venue.")
                return

        # [L-03] Bloquea la reducción de aforo si las entradas ya vendidas superan el nuevo límite
        if nueva_capacidad < venue["capacidad_maxima"]:
            eventos_del_venue = [e for e in self.repo.listar("eventos") if e["venue_id"] == id_venue]
            entradas_activas = self.repo.listar("entradas")
            for ev in eventos_del_venue:
                vendidas = sum(1 for e in entradas_activas if e["evento_id"] == ev["id"])
                if nueva_capacidad < vendidas:
                    print(f"[❌ ERROR] No se puede reducir el aforo: el evento '{ev['nombre']}' ya tiene {vendidas} entradas vendidas.")
                    return

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
    # D - ELIMINAR (Eliminar Venue Lógico - VERSIÓN CON REINTENTOS)
    # =====================================================================
    def eliminar(self):
        print("\n--- ELIMINAR VENUE ---")
            
        while True:
            id_venue = pedir_entero("Ingrese el ID del venue a eliminar o 0 para cancelar")

            if id_venue == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            venue = self.repo.buscar_por_id("venues", id_venue)

            if venue is None:
                print(f"[❌ ERROR] No existe un venue activo con el ID {id_venue}.")
                print("Por favor, intente con otro ID.\n")
                continue

            eventos = self.repo.listar("eventos")

            for evento in eventos:
                if evento["venue_id"] == id_venue:
                    print("[❌ ERROR] No se puede eliminar este venue porque tiene eventos activos asignados.")
                    return

            # [L-12] Confirmación explícita antes de ejecutar la eliminación lógica
            confirmacion = input(f"¿Confirma eliminar el venue '{venue['nombre']}'? (s/n): ").strip().lower()
            if confirmacion != "s":
                print("[ℹ INFO] Operación cancelada por el usuario.")
                return

            eliminado = self.repo.eliminar_logico("venues", id_venue)

            if eliminado:
                print("[✔ ÉXITO] Venue eliminado lógicamente.")
                break