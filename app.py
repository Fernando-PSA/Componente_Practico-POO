from repository.repo_json import RepoJson

from services.organizador_service import OrganizadorService
from services.venue_service import VenueService
from services.patrocinador_service import PatrocinadorService
from services.asistente_service import AsistenteService
from services.evento_service import EventoService
from services.entrada_service import EntradaService


# =========================================
# CONEXION CON EL ARCHIVO JSON
# =========================================
repo = RepoJson("data/db.json")


# =========================================
# INSTANCIAS DE LOS SERVICES
# =========================================
organizador_service = OrganizadorService(repo)
venue_service = VenueService(repo)
patrocinador_service = PatrocinadorService(repo)
asistente_service = AsistenteService(repo)
evento_service = EventoService(repo)
entrada_service = EntradaService(repo)


# =========================================
# MENU ORGANIZADORES
# =========================================
def menu_organizadores():

    opcion = ""

    while opcion != "0":

        print("\n========== MENÚ ORGANIZADORES ==========")
        print("1. Registrar organizador")
        print("2. Listar organizadores")
        print("3. Modificar organizador")
        print("4. Eliminar organizador")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            organizador_service.registrar()

        elif opcion == "2":
            organizador_service.listar()

        elif opcion == "3":
            organizador_service.modificar()

        elif opcion == "4":
            organizador_service.eliminar()

        elif opcion == "0":
            print("Volviendo al menú principal...")

        else:
            print("Opción incorrecta.")


# =========================================
# MENU VENUES
# =========================================
def menu_venues():

    opcion = ""

    while opcion != "0":

        print("\n========== MENÚ VENUES ==========")
        print("1. Registrar venue")
        print("2. Listar venues")
        print("3. Modificar venue")
        print("4. Eliminar venue")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            venue_service.registrar()

        elif opcion == "2":
            venue_service.listar()

        elif opcion == "3":
            venue_service.modificar()

        elif opcion == "4":
            venue_service.eliminar()

        elif opcion == "0":
            print("Volviendo al menú principal...")

        else:
            print("Opción incorrecta.")


# =========================================
# MENU PATROCINADORES
# =========================================
def menu_patrocinadores():

    opcion = ""

    while opcion != "0":

        print("\n========== MENÚ PATROCINADORES ==========")
        print("1. Registrar patrocinador")
        print("2. Listar patrocinadores")
        print("3. Modificar patrocinador")
        print("4. Eliminar patrocinador")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            patrocinador_service.registrar()

        elif opcion == "2":
            patrocinador_service.listar()

        elif opcion == "3":
            patrocinador_service.modificar()

        elif opcion == "4":
            patrocinador_service.eliminar()

        elif opcion == "0":
            print("Volviendo al menú principal...")

        else:
            print("Opción incorrecta.")


# =========================================
# MENU ASISTENTES
# =========================================
def menu_asistentes():

    opcion = ""

    while opcion != "0":

        print("\n========== MENÚ ASISTENTES ==========")
        print("1. Registrar asistente")
        print("2. Listar asistentes")
        print("3. Modificar asistente")
        print("4. Eliminar asistente")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            asistente_service.registrar()

        elif opcion == "2":
            asistente_service.listar()

        elif opcion == "3":
            asistente_service.modificar()

        elif opcion == "4":
            asistente_service.eliminar()

        elif opcion == "0":
            print("Volviendo al menú principal...")

        else:
            print("Opción incorrecta.")


# =========================================
# MENU EVENTOS
# =========================================
def menu_eventos():

    opcion = ""

    while opcion != "0":

        print("\n========== MENÚ EVENTOS ==========")
        print("1. Registrar evento")
        print("2. Listar eventos")
        print("3. Modificar evento")
        print("4. Eliminar evento")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            evento_service.registrar()

        elif opcion == "2":
            evento_service.listar()

        elif opcion == "3":
            evento_service.modificar()

        elif opcion == "4":
            evento_service.eliminar()

        elif opcion == "0":
            print("Volviendo al menú principal...")

        else:
            print("Opción incorrecta.")


# =========================================
# MENU ENTRADAS
# =========================================
def menu_entradas():

    opcion = ""

    while opcion != "0":

        print("\n========== MENÚ ENTRADAS ==========")
        print("1. Emitir entrada")
        print("2. Listar entradas")
        print("3. Cancelar entrada")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            entrada_service.registrar()

        elif opcion == "2":
            entrada_service.listar()

        elif opcion == "3":
            entrada_service.eliminar()

        elif opcion == "0":
            print("Volviendo al menú principal...")

        else:
            print("Opción incorrecta.")


# =========================================
# MENU PRINCIPAL
# =========================================
def menu_principal():

    opcion = ""

    while opcion != "0":

        print("\n========== SISTEMA GESTIÓN DE EVENTOS ==========")
        print("1. Gestión de organizadores")
        print("2. Gestión de venues")
        print("3. Gestión de patrocinadores")
        print("4. Gestión de asistentes")
        print("5. Gestión de eventos")
        print("6. Gestión de entradas")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_organizadores()

        elif opcion == "2":
            menu_venues()

        elif opcion == "3":
            menu_patrocinadores()

        elif opcion == "4":
            menu_asistentes()

        elif opcion == "5":
            menu_eventos()

        elif opcion == "6":
            menu_entradas()

        elif opcion == "0":
            print("Saliendo del sistema...")

        else:
            print("Opción incorrecta.")


# =========================================
# INICIO DEL SISTEMA
# =========================================
menu_principal()