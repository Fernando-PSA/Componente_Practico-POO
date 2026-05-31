from models.asistente import Asistente
from utils.generador_id import generar_id_secuencial
# Importamos las funciones inteligentes de validación
from utils.validaciones import (
    pedir_cedula, 
    pedir_solo_letras, 
    pedir_correo, 
    pedir_entero, 
    pedir_alfanumerico
)


class AsistenteService:

    def __init__(self, repo):
        self.repo = repo

    # =====================================================================
    # C - CREAR (Registrar Asistente)
    # =====================================================================
    def registrar(self):
        print("\n--- REGISTRAR ASISTENTE ---")
        
        # Eliminamos los dos puntos manuales para delegar el formato a validaciones.py
        cedula = pedir_cedula("Cédula", repo=self.repo, coleccion="asistentes")
        nombres = pedir_solo_letras("Nombres")
        apellidos = pedir_solo_letras("Apellidos")
        correo = pedir_correo("Correo electrónico", repo=self.repo, coleccion="asistentes")
        direccion = pedir_alfanumerico("Dirección")

        # Obtener lista completa para el ID secuencial
        asistentes_en_db = self.repo.listar("asistentes", solo_activos=False)

        # Crear instancia del modelo de dominio
        asistente = Asistente(
            generar_id_secuencial(asistentes_en_db),
            cedula,
            nombres,
            apellidos,
            correo,
            direccion,
            True
        )

        # Guardar persistencia en el archivo JSON
        self.repo.guardar("asistentes", asistente.convertir_a_diccionario())
        print("[✔ ÉXITO] Asistente registrado correctamente.")

    # =====================================================================
    # R - LEER (Listar Asistentes)
    # =====================================================================
    def listar(self):
        print("\n--- LISTADO DE ASISTENTES ---")
        asistentes = self.repo.listar("asistentes")

        if len(asistentes) == 0:
            print("[ℹ INFO] No existen asistentes registrados.")
            return

        for asistente in asistentes:
            print(
                f"ID: {asistente['id']} | "
                f"Cédula: {asistente['cedula']} | "
                f"Nombres: {asistente['nombres']} {asistente['apellidos']} | "
                f"Correo: {asistente['correo']} | "
                f"Dirección: {asistente['direccion']}"
            )

    # =====================================================================
    # U - ACTUALIZAR (Modificar Asistente - VERSIÓN CON REINTENTOS)
    # =====================================================================
    def modificar(self):
        print("\n--- MODIFICAR ASISTENTE ---")
        
        # 🔄 BUCLE 1: Reintenta pedir el ID hasta que exista en la base de datos
        while True:
            id_asistente = pedir_entero("Ingrese el ID del asistente a modificar o 0 para cancelar")

            if id_asistente == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            asistente = self.repo.buscar_por_id("asistentes", id_asistente)

            if asistente is None:
                print(f"[❌ ERROR] No existe un asistente activo con el ID {id_asistente}.")
                print("Por favor, verifique e intente con un ID válido de la lista.\n")
                continue # 🔄 Mantiene al usuario en el flujo de solicitud
                        
            break # 🏁 Si el ID existe, rompe el bucle para editar los campos

        print("Deje vacío un campo si no desea modificarlo (Presione Enter).")
        
        # 🔄 BUCLE 2: Control interactivo de unicidad para la Cédula nueva
        while True:
            nueva_cedula = pedir_cedula("Cédula nueva", valor_actual=asistente['cedula'], repo=self.repo, coleccion="asistentes", id_registro=id_asistente)
            break

        nuevos_nombres = pedir_solo_letras("Nombres nuevos", valor_actual=asistente['nombres'])
        nuevos_apellidos = pedir_solo_letras("Apellidos nuevos", valor_actual=asistente['apellidos'])

        # 🔄 BUCLE 3: Control interactivo de unicidad para el Correo nuevo
        while True:
            nuevo_correo = pedir_correo("Correo nuevo", valor_actual=asistente['correo'], repo=self.repo, coleccion="asistentes", id_registro=id_asistente)
            break

        nuevo_direccion = pedir_alfanumerico("Dirección nueva", valor_actual=asistente['direccion'])

        nuevos_datos = {
            "cedula": nueva_cedula,
            "nombres": nuevos_nombres,
            "apellidos": nuevos_apellidos,
            "correo": nuevo_correo,
            "direccion": nuevo_direccion,
            "estado": True
        }

        self.repo.actualizar("asistentes", id_asistente, nuevos_datos)
        print("[✔ ÉXITO] Asistente modificado correctamente.")

    # =====================================================================
    # D - ELIMINAR (Eliminar Asistente Lógico - VERSIÓN CON REINTENTOS)
    # =====================================================================
    def eliminar(self):
        print("\n--- ELIMINAR ASISTENTE ---")
            
        while True:
            id_asistente = pedir_entero("Ingrese el ID del asistente a eliminar o 0 para cancelar")

            if id_asistente == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            asistente = self.repo.buscar_por_id("asistentes", id_asistente)

            if asistente is None:
                print(f"[❌ ERROR] No existe un asistente activo con el ID {id_asistente}.")
                print("Por favor, intente con otro ID de la lista.\n")
                continue

            # [L-11] Incluye historial completo (activas e inactivas) para preservar la integridad
            #         referencial: una entrada huérfana sin asistente rompería los reportes históricos
            entradas = self.repo.listar("entradas", solo_activos=False)

            for entrada in entradas:
                if entrada["asistente_id"] == id_asistente:
                    print("[❌ ERROR] No se puede eliminar este asistente porque tiene historial de entradas registradas (activas o canceladas).")
                    return

            # [L-12] Confirmación explícita antes de ejecutar la eliminación lógica
            confirmacion = input(f"¿Confirma eliminar al asistente '{asistente['nombres']} {asistente['apellidos']}'? (s/n): ").strip().lower()
            if confirmacion != "s":
                print("[ℹ INFO] Operación cancelada por el usuario.")
                return

            eliminado = self.repo.eliminar_logico("asistentes", id_asistente)

            if eliminado:
                print("[✔ ÉXITO] Asistente eliminado lógicamente.")
                break