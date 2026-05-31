from models.organizador import Organizador
from utils.generador_id import generar_id_secuencial
# Importamos las funciones limpias de validación externa
from utils.validaciones import (
    pedir_cedula, 
    pedir_solo_letras, 
    pedir_correo, 
    pedir_entero, 
    pedir_telefono
)


class OrganizadorService:

    def __init__(self, repo):
        self.repo = repo

    # =====================================================================
    # C - CREAR (Registrar Organizador)
    # =====================================================================
    def registrar(self):
        print("\n--- REGISTRAR ORGANIZADOR ---")
        
        # Cada petición crítica se envuelve en su lógica de negocio para reintentar
        cedula = pedir_cedula("Cédula", repo=self.repo, coleccion="organizadores")
        nombres = pedir_solo_letras("Nombres")
        apellidos = pedir_solo_letras("Apellidos")
        correo = pedir_correo("Correo electrónico", repo=self.repo, coleccion="organizadores")
        telefono = pedir_telefono("Teléfono celular")

        # Obtener todos los registros para calcular el ID secuencial desde 1
        organizadores_en_db = self.repo.listar("organizadores", solo_activos=False)

        # Creación de la instancia del modelo de dominio
        organizador = Organizador(
            generar_id_secuencial(organizadores_en_db),
            cedula,
            nombres,
            apellidos,
            correo,
            telefono,
            True
        )

        # Persistencia en la base de datos JSON
        self.repo.guardar("organizadores", organizador.convertir_a_diccionario())
        print("[✔ ÉXITO] Organizador registrado correctamente.")

    # =====================================================================
    # R - LEER (Listar Organizadores)
    # =====================================================================
    def listar(self):
        print("\n--- LISTADO DE ORGANIZADORES ---")
        organizadores = self.repo.listar("organizadores")

        if len(organizadores) == 0:
            print("[ℹ INFO] No existen organizadores registrados.")
            return

        for org in organizadores:
            print(
                f"ID: {org['id']} | "
                f"Cédula: {org['cedula']} | "
                f"Nombres: {org['nombres']} {org['apellidos']} | "
                f"Correo: {org['correo']} | "
                f"Teléfono: {org['telefono']}"
            )

    # =====================================================================
    # U - ACTUALIZAR (Modificar Organizador - VERSIÓN COMPLETA CON REINTENTOS)
    # =====================================================================
    def modificar(self):
        print("\n--- MODIFICAR ORGANIZADOR ---")
        
        # 🔄 BUCLE 1: Reintenta el ID hasta que exista en el archivo JSON
        while True:
            id_organizador = pedir_entero("Ingrese el ID del organizador a modificar o 0 para cancelar")

            if id_organizador == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            organizador = self.repo.buscar_por_id("organizadores", id_organizador)

            if organizador is None:
                print(f"[❌ ERROR] No existe un organizador activo con el ID {id_organizador}.")
                print("Por favor, intente con un ID válido de la lista.\n")
                continue # 🔄 Se queda en el bucle pidiendo el ID de nuevo
                    
            break # 🏁 Si existe el ID, rompe el bucle y continúa

        print("Deje vacío un campo si no desea modificarlo (Presione Enter).")
        
        # 🔄 BUCLE 2: Captura y valida la Cédula nueva controlando duplicados
        while True:
            nueva_cedula = pedir_cedula("Cédula nueva", valor_actual=organizador['cedula'], repo=self.repo, coleccion="organizadores", id_registro=id_organizador)
            break

        nuevos_nombres = pedir_solo_letras("Nombres nuevos", valor_actual=organizador['nombres'])
        nuevos_apellidos = pedir_solo_letras("Apellidos nuevos", valor_actual=organizador['apellidos'])

        # 🔄 BUCLE 3: Captura y valida el Correo nuevo controlando duplicados
        while True:
            nuevo_correo = pedir_correo("Correo nuevo", valor_actual=organizador['correo'], repo=self.repo, coleccion="organizadores", id_registro=id_organizador)
            break

        nuevo_telefono = pedir_telefono("Teléfono nuevo", valor_actual=organizador['telefono'])

        nuevos_datos = {
            "cedula": nueva_cedula,
            "nombres": nuevos_nombres,
            "apellidos": nuevos_apellidos,
            "correo": nuevo_correo,
            "telefono": nuevo_telefono,
            "estado": True
        }

        self.repo.actualizar("organizadores", id_organizador, nuevos_datos)
        print("[✔ ÉXITO] Organizador modificado correctamente.")

    # =====================================================================
    # D - ELIMINAR (Eliminar Organizador Lógico)
    # =====================================================================
    def eliminar(self):
        print("\n--- ELIMINAR ORGANIZADOR ---")
            
        while True:
            id_organizador = pedir_entero("Ingrese el ID del organizador a eliminar o 0 para cancelar")

            if id_organizador == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            organizador = self.repo.buscar_por_id("organizadores", id_organizador)

            if organizador is None:
                print(f"[❌ ERROR] No existe un organizador activo con el ID {id_organizador}.")
                print("Por favor, intente con otro ID.\n")
                continue

            eventos = self.repo.listar("eventos")

            for evento in eventos:
                if evento["organizador_id"] == id_organizador:
                    print("[❌ ERROR] No se puede eliminar este organizador porque tiene eventos activos asignados.")
                    return

            eliminado = self.repo.eliminar_logico("organizadores", id_organizador)

            if eliminado:
                print("[✔ ÉXITO] Organizador eliminado lógicamente.")
                break