from models.patrocinador import Patrocinador
from utils.generador_id import generar_id_secuencial
# Importamos las utilidades de validación correspondientes
from utils.validaciones import (
    pedir_empresa, 
    pedir_telefono,  
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

        # [L-06] Unicidad del nombre de empresa (case-insensitive) para evitar patrocinadores duplicados
        while True:
            empresa = pedir_empresa("Empresa")
            patrocinadores_activos = self.repo.listar("patrocinadores")
            duplicado = next((p for p in patrocinadores_activos if p["empresa"].lower() == empresa.lower()), None)
            if duplicado:
                print(f"[❌ ERROR] Ya existe un patrocinador registrado con la empresa '{empresa}'. Ingrese otro.")
                continue
            break

        telefono = pedir_telefono("Teléfono")
        aporte = pedir_aporte_economico("Aporte económico")

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
    # U - ACTUALIZAR (Modificar Patrocinador - VERSIÓN CON REINTENTOS)
    # =====================================================================
    def modificar(self):
        print("\n--- MODIFICAR PATROCINADOR ---")

        # 🔄 BUCLE 1: Reintenta pedir el ID hasta que exista en el archivo db.json
        while True:
            id_patrocinador = pedir_entero("Ingrese el ID del patrocinador a modificar o 0 para cancelar")

            if id_patrocinador == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            patrocinador = self.repo.buscar_por_id("patrocinadores", id_patrocinador)

            if patrocinador is None:
                print(f"[❌ ERROR] No existe un patrocinador activo con el ID {id_patrocinador}.")
                print("Por favor, verifique e intente con un ID válido de la lista.\n")
                continue # 🔄 Se queda en la línea inferior solicitando el ID otra vez
                
            break  # 🏁 Si existe el ID, rompe el ciclo para continuar con la captura

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
    # D - ELIMINAR (Eliminar Patrocinador Lógico - VERSIÓN CON REINTENTOS)
    # =====================================================================
    def eliminar(self):
        print("\n--- ELIMINAR PATROCINADOR ---")

        while True:
            id_patrocinador = pedir_entero("Ingrese el ID del patrocinador a eliminar o 0 para cancelar")

            if id_patrocinador == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            patrocinador = self.repo.buscar_por_id("patrocinadores", id_patrocinador)

            if patrocinador is None:
                print(f"[❌ ERROR] No existe un patrocinador activo con el ID {id_patrocinador}.")
                print("Por favor, intente con otro ID de la lista.\n")
                continue

            eventos = self.repo.listar("eventos")

            for evento in eventos:
                if id_patrocinador in evento.get("patrocinadores_ids", []):
                    print("[❌ ERROR] No se puede eliminar este patrocinador porque está asignado a eventos activos.")
                    return

            # [L-12] Confirmación explícita antes de ejecutar la eliminación lógica
            confirmacion = input(f"¿Confirma eliminar al patrocinador '{patrocinador['empresa']}'? (s/n): ").strip().lower()
            if confirmacion != "s":
                print("[ℹ INFO] Operación cancelada por el usuario.")
                return

            eliminado = self.repo.eliminar_logico("patrocinadores", id_patrocinador)

            if eliminado:
                print("[✔ ÉXITO] Patrocinador eliminado lógicamente.")
                break