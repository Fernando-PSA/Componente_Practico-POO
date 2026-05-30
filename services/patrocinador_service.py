import re

from models.patrocinador import Patrocinador
from utils.generador_id import generar_id_secuencial
from utils.validaciones import pedir_empresa, pedir_telefono, pedir_entero_positivo, pedir_entero


class PatrocinadorService:

    # Constructor de la clase
    def __init__(self, repo):
        self.repo = repo

    # Metodo para registrar patrocinadores
    def registrar(self):
        print("\n--- REGISTRAR PATROCINADOR ---")

        empresa = pedir_empresa("Empresa: ")
        telefono = pedir_telefono("Teléfono: ")
        aporte = pedir_entero_positivo("Aporte económico: ")

        # Obtener patrocinadores registrados
        patrocinadores = self.repo.listar(
            "patrocinadores",
            solo_activos=False
        )

        # Crear objeto Patrocinador
        patrocinador = Patrocinador(
            generar_id_secuencial(patrocinadores),
            empresa,
            telefono,
            aporte,
            True
        )

        # Guardar patrocinador
        self.repo.guardar("patrocinadores", patrocinador.convertir_a_diccionario())

        print("Patrocinador registrado correctamente.")

    # Metodo para listar patrocinadores
    def listar(self):
        print("\n--- LISTADO DE PATROCINADORES ---")

        patrocinadores = self.repo.listar("patrocinadores")

        if len(patrocinadores) == 0:
            print("No existen patrocinadores registrados.")
            return

        for patrocinador in patrocinadores:
            print(
                f"ID: {patrocinador['id']} | "
                f"Empresa: {patrocinador['empresa']} | "
                f"Teléfono: {patrocinador['telefono']} | "
                f"Aporte: ${patrocinador['aporte']}"
            )

    # Metodo para modificar patrocinadores
    def modificar(self):
        print("\n--- MODIFICAR PATROCINADOR ---")

        while True:
            id_patrocinador = pedir_entero("Ingrese el ID del patrocinador a modificar: ")

            patrocinador = self.repo.buscar_por_id("patrocinadores", id_patrocinador)

            if patrocinador is None:
                print("Error. No existe un patrocinador activo con ese ID.")

                continue

            break

        print("Deje vacío un campo si no desea modificarlo.")

        while True:
            nueva_empresa = input(f"Empresa actual ({patrocinador['empresa']}): ").strip()

            if nueva_empresa == "":
                nueva_empresa = patrocinador["empresa"]
                break

            if not re.fullmatch(r"[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s.,&+_/'’()-]+",nueva_empresa):
                print("Error. Nombre de empresa inválido.")
                continue
            
            if not re.search(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ]", nueva_empresa):
                print("Error. La empresa debe contener al menos una letra.")
                continue

            break

        while True:
            nuevo_telefono = input(f"Teléfono actual ({patrocinador['telefono']}): ").strip()

            if nuevo_telefono == "":
                nuevo_telefono = patrocinador["telefono"]
                break

            if not nuevo_telefono.isdigit():
                print("Error. El teléfono solo debe contener números.")
                continue

            if len(nuevo_telefono) != 10:
                print("Error. El teléfono debe tener 10 dígitos.")
                continue

            break

        while True:
            nuevo_aporte = input(f"Aporte actual ({patrocinador['aporte']}): ").strip()

            if nuevo_aporte == "":
                nuevo_aporte = patrocinador["aporte"]
                break

            if not nuevo_aporte.isdigit():
                print("Error. El aporte solo permite números enteros.")
                continue

            nuevo_aporte = int(nuevo_aporte)

            if nuevo_aporte <= 0:
                print("Error. El aporte debe ser mayor a 0.")
                continue

            break

        nuevos_datos = {
            "empresa": nueva_empresa,
            "telefono": nuevo_telefono,
            "aporte": nuevo_aporte,
            "estado": True
        }

        self.repo.actualizar(
            "patrocinadores",
            id_patrocinador,
            nuevos_datos
        )

        print("Patrocinador modificado correctamente.")

    # Metodo para eliminar patrocinadores
    def eliminar(self):
        print("\n--- ELIMINAR PATROCINADOR ---")

        id_patrocinador = pedir_entero("Ingrese el ID del patrocinador a eliminar: ")
        
        eliminado = self.repo.eliminar_logico("patrocinadores", id_patrocinador)

        if eliminado:
            print("Patrocinador eliminado lógicamente.")
        else:
            print("No se encontró el patrocinador.")