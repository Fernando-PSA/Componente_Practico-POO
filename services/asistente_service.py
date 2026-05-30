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
        
        # Enviamos el repo y la colección para que valide la unicidad automáticamente internamente
        cedula = pedir_cedula("Cédula: ", repo=self.repo, coleccion="asistentes")
        nombres = pedir_solo_letras("Nombres: ")
        apellidos = pedir_solo_letras("Apellidos: ")
        correo = pedir_correo("Correo electrónico: ", repo=self.repo, coleccion="asistentes")
        direccion = pedir_alfanumerico("Dirección: ")

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
    # U - ACTUALIZAR (Modificar Asistente)
    # =====================================================================
    def modificar(self):
        print("\n--- MODIFICAR ASISTENTE ---")
        id_asistente = pedir_entero("Ingrese el ID del asistente a modificar: ")
        asistente = self.repo.buscar_por_id("asistentes", id_asistente)

        if asistente is None:
            print("[❌ ERROR] No existe un asistente activo con ese ID.")
            return

        print("Deje vacío un campo si no desea modificarlo (Presione Enter).")
        
        # Pasamos el 'valor_actual' para que la función sepa que es una modificación opcional
        # Pasamos el 'id_registro' para evitar falsos positivos de duplicados consigo mismo
        nueva_cedula = pedir_cedula("Cédula nueva", valor_actual=asistente['cedula'], repo=self.repo, coleccion="asistentes", id_registro=id_asistente)
        nuevos_nombres = pedir_solo_letras("Nombres nuevos", valor_actual=asistente['nombres'])
        nuevos_apellidos = pedir_solo_letras("Apellidos nuevos", valor_actual=asistente['apellidos'])
        nuevo_correo = pedir_correo("Correo nuevo", valor_actual=asistente['correo'], repo=self.repo, coleccion="asistentes", id_registro=id_asistente)
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
    # D - ELIMINAR (Eliminar Asistente Logico)
    # =====================================================================
    def eliminar(self):
        print("\n--- ELIMINAR ASISTENTE ---")
        id_asistente = pedir_entero("Ingrese el ID del asistente a eliminar: ")

        eliminado = self.repo.eliminar_logico("asistentes", id_asistente)

        if eliminado:
            print("[✔ ÉXITO] Asistente eliminado lógicamente.")
        else:
            print("[❌ ERROR] No se encontró el asistente o ya se encuentra inactivo.")