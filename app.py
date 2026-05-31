from repository.repo_json import RepoJson

from services.organizador_service import OrganizadorService
from services.venue_service import VenueService
from services.patrocinador_service import PatrocinadorService
from services.asistente_service import AsistenteService
from services.evento_service import EventoService
from services.entrada_service import EntradaService


# =====================================================
# CONEXIÓN CON EL ARCHIVO JSON (PERSISTENCIA)
# =====================================================
repo = RepoJson("data/db.json")


# =====================================================
# INSTANCIAS DE LOS SERVICIOS DE CAPA DE NEGOCIO
# =====================================================
organizador_service = OrganizadorService(repo)
venue_service = VenueService(repo)
patrocinador_service = PatrocinadorService(repo)
asistente_service = AsistenteService(repo)
evento_service = EventoService(repo)
entrada_service = EntradaService(repo)


# =====================================================
# SUBMENÚ: ORGANIZADORES
# =====================================================
def menu_organizadores():
    opcion = ""
    while opcion != "0":
        print("\n========== MENÚ ORGANIZADORES ==========")
        print("1. Registrar organizador")
        print("2. Listar organizadores")
        print("3. Modificar organizador")
        print("4. Eliminar organizador")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            organizador_service.registrar()
        elif opcion == "2":
            organizador_service.listar()
        elif opcion == "3":
            organizador_service.modificar()
        elif opcion == "4":
            organizador_service.eliminar()
        elif opcion == "0":
            print("[ℹ INFO] Volviendo al menú principal...")
        else:
            print("[❌ ERROR] Opción incorrecta. Ingrese un número del menú.")


# =====================================================
# SUBMENÚ: VENUES (LUGARES)
# =====================================================
def menu_venues():
    opcion = ""
    while opcion != "0":
        print("\n========== MENÚ VENUES ==========")
        print("1. Registrar venue")
        print("2. Listar venues")
        print("3. Modificar venue")
        print("4. Eliminar venue")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            venue_service.registrar()
        elif opcion == "2":
            venue_service.listar()
        elif opcion == "3":
            venue_service.modificar()
        elif opcion == "4":
            venue_service.eliminar()
        elif opcion == "0":
            print("[ℹ INFO] Volviendo al menú principal...")
        else:
            print("[❌ ERROR] Opción incorrecta. Ingrese un número del menú.")


# =====================================================
# SUBMENÚ: PATROCINADORES
# =====================================================
def menu_patrocinadores():
    opcion = ""
    while opcion != "0":
        print("\n========== MENÚ PATROCINADORES ==========")
        print("1. Registrar patrocinador")
        print("2. Listar patrocinadores")
        print("3. Modificar patrocinador")
        print("4. Eliminar patrocinador")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            patrocinador_service.registrar()
        elif opcion == "2":
            patrocinador_service.listar()
        elif opcion == "3":
            patrocinador_service.modificar()
        elif opcion == "4":
            patrocinador_service.eliminar()
        elif opcion == "0":
            print("[ℹ INFO] Volviendo al menú principal...")
        else:
            print("[❌ ERROR] Opción incorrecta. Ingrese un número del menú.")


# =====================================================
# SUBMENÚ: ASISTENTES
# =====================================================
def menu_asistentes():
    opcion = ""
    while opcion != "0":
        print("\n========== MENÚ ASISTENTES ==========")
        print("1. Registrar asistente")
        print("2. Listar asistentes")
        print("3. Modificar asistente")
        print("4. Eliminar asistente")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            asistente_service.registrar()
        elif opcion == "2":
            asistente_service.listar()
        elif opcion == "3":
            asistente_service.modificar()
        elif opcion == "4":
            asistente_service.eliminar()
        elif opcion == "0":
            print("[ℹ INFO] Volviendo al menú principal...")
        else:
            print("[❌ ERROR] Opción incorrecta. Ingrese un número del menú.")


# =====================================================
# SUBMENÚ: EVENTOS (Incluye operaciones de consulta)
# =====================================================
def menu_eventos():
    opcion = ""
    while opcion != "0":
        print("\n========== MENÚ EVENTOS ==========")
        print("1. Registrar evento")
        print("2. Listar eventos")
        print("3. Modificar evento")
        print("4. Eliminar evento")
        print("5. Reporte: Ver ingresos financieros por evento (Entradas + Patrocinios)")
        print("6. Consulta: Filtrar eventos (Por ciudad o rango de fechas)")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            evento_service.registrar()
        elif opcion == "2":
            evento_service.listar()
        elif opcion == "3":
            evento_service.modificar()
        elif opcion == "4":
            evento_service.eliminar()
        elif opcion == "5":
            evento_service.ingresos_por_evento()  # Operación adicional de Ingresos
        elif opcion == "6":
            evento_service.filtrar_eventos()       # Operación adicional de Filtrado
        elif opcion == "0":
            print("[ℹ INFO] Volviendo al menú principal...")
        else:
            print("[❌ ERROR] Opción incorrecta. Ingrese un número del menú.")


# =====================================================
# SUBMENÚ: ENTRADAS (Incluye ordenamiento de asistentes)
# =====================================================
def menu_entradas():
    opcion = ""
    while opcion != "0":
        print("\n========== MENÚ ENTRADAS ==========")
        print("1. Emitir nueva entrada (Control de Aforo)")
        print("2. Listar todas las entradas emitidas")
        print("3. Modificar precio de entrada existente")  # [L-13]
        print("4. Cancelar/Anular entrada existente")
        print("5. Reporte: Listar asistentes ordenados (Por apellido o código)")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            entrada_service.registrar()
        elif opcion == "2":
            entrada_service.listar()
        elif opcion == "3":
            entrada_service.modificar()          # [L-13] Nueva opción de modificación
        elif opcion == "4":
            entrada_service.eliminar()
        elif opcion == "5":
            entrada_service.listar_asistentes_ordenada()
        elif opcion == "0":
            print("[ℹ INFO] Volviendo al menú principal...")
        else:
            print("[❌ ERROR] Opción incorrecta. Ingrese un número del menú.")


# =====================================================
# MENÚ PRINCIPAL DEL SISTEMA
# =====================================================
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
        print("0. Salir del programa")

        opcion = input("Seleccione una opción: ").strip()

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
            print("[ℹ INFO] Saliendo del sistema de gestión. ¡Hasta pronto!")
        else:
            print("[❌ ERROR] Opción incorrecta. Seleccione una opción válida de la lista.")


# =====================================================
# ENTRADA DE EJECUCIÓN PRINCIPAL
# =====================================================
if __name__ == "__main__":
    menu_principal()