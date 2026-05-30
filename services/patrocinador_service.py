from models.patrocinador import Patrocinador
from utils.generador_id import generar_id_secuencial
# Importamos las utilidades de validación correspondientes
from utils.validaciones import (
    pedir_empresa, 
    pedir_telefono, 
    pedir_entero_positivo, 
    pedir_entero,
    pedir_aporte_economico
)


class PatrocinadorService:

    # Constructor de la clase
    def __init__(self, repo):
        self.repo = repo

    # =====================================================================
    # C - CREAR (Registrar Patrocinador)
    # =====================================================================
    def registrar(self):
        print("\n--- REGISTRAR PATROCINADOR ---")

        # Invocamos las validaciones obligatorias de registro
        empresa = pedir_empresa("Empresa: ")
        telefono = pedir_telefono("Teléfono: ")
        aporte = pedir_aporte_economico("Aporte económico: ")

        # Obtener patrocinadores registrados para el ID autoincremental
        patrocinadores = self.repo.listar("patrocinadores", solo_activos=False)

        # Crear objeto Patrocinador
        patrocinador = Patrocinador(
            generar_id_secuencial(patrocinadores),
            empresa,
            telefono,
            aporte,
            True
        )

        # Guardar patrocinador en persistencia JSON
        self.repo.guardar("patrocinadores", patrocinador.convertir_a_diccionario())
        print("[✔ ÉXITO] Patrocinador registrado correctamente.")

    # =====================================================================
    # R - LEER (Listar Patrocinadores)
    # =====================================================================
    def listar(self):
        print("\n--- LISTADO DE PATROCINADORES ---")

        patrocinadores = self.repo.listar("patrocinadores")

        if len(patrocinadores) == 0:
            print("[ℹ INFO] No existen patrocinadores registrados.")
            return

        for patrocinador in patrocinadores:
            print(
                f"ID: {patrocinador['id']} | "
                f"Empresa: {patrocinador['empresa']} | "
                f"Teléfono: {patrocinador['telefono']} | "
                f"Aporte: ${patrocinador['aporte']}"
            )

    # =====================================================================
    # U - ACTUALIZAR (Modificar Patrocinador)
    # =====================================================================
    def modificar(self):
        print("\n--- MODIFICAR PATROCINADOR ---")

        id_patrocinador = pedir_entero("Ingrese el ID del patrocinador a modificar: ")
        patrocinador = self.repo.buscar_por_id("patrocinadores", id_patrocinador)

        if patrocinador is None:
            print("[❌ ERROR] No existe un patrocinador activo con ese ID.")
            return

        print("Deje vacío un campo si no desea modificarlo (Presione Enter).")

        # Invocamos las funciones pasando 'valor_actual' para que actúen en modo Modificación (Opcional)
        nueva_empresa = pedir_empresa("Empresa nueva", valor_actual=patrocinador['empresa'])
        nuevo_telefono = pedir_telefono("Teléfono nuevo", valor_actual=patrocinador['telefono'])
        nuevo_aporte = pedir_aporte_economico("Aporte nuevo", valor_actual=patrocinador['aporte'])

        nuevos_datos = {
            "empresa": nueva_empresa,
            "telefono": nuevo_telefono,
            "aporte": nuevo_aporte,
            "estado": True
        }

        self.repo.actualizar("patrocinadores", id_patrocinador, nuevos_datos)
        print("[✔ ÉXITO] Patrocinador modificado correctamente.")

    # =====================================================================
    # D - ELIMINAR (Eliminar Patrocinador Lógico)
    # =====================================================================
    def eliminar(self):
        print("\n--- ELIMINAR PATROCINADOR ---")

        id_patrocinador = pedir_entero("Ingrese el ID del patrocinador a eliminar: ")
        
        eliminado = self.repo.eliminar_logico("patrocinadores", id_patrocinador)

        if eliminado:
            print("[✔ ÉXITO] Patrocinador eliminado lógicamente.")
        else:
            print("[❌ ERROR] No se encontró el patrocinador o ya se encuentra inactivo.")