import re

from models.asistente import Asistente
from utils.generador_id import generar_id_secuencial
from utils.validaciones import pedir_cedula, pedir_solo_letras, pedir_correo, pedir_entero, pedir_alfanumerico, validar_cedula_ecuatoriana


class AsistenteService:

    # Constructor de la clase
    def __init__(self, repo):
        self.repo = repo

    # Metodo para registrar asistentes
    def registrar(self):
        print("\n--- REGISTRAR ASISTENTE ---")
        while True:
            cedula = pedir_cedula("Cédula: ")

            # Verificar si ya existe un asistente con esa cedula
            asistente_existente = self.repo.buscar_por_campo(
                "asistentes",
                "cedula",
                cedula
            )
        
            if asistente_existente:
                print("Ya existe un asistente activo con esa cédula.")
                continue
            
            break

        nombres = pedir_solo_letras("Nombres: ")
        apellidos = pedir_solo_letras("Apellidos: ")
        
        while True:
            correo = pedir_correo("Correo electrónico: ")

            existente = self.repo.buscar_por_campo(
                "asistentes",
                "correo",
                correo
            )

            if existente:
                print("Ya existe un asistente con ese correo.")
                continue

            break
        
        direccion = pedir_alfanumerico("Dirección: ")

        # Obtener asistentes registrados
        asistentes = self.repo.listar(
            "asistentes",
            solo_activos=False
        )

        # Crear objeto Asistente
        asistente = Asistente(
            generar_id_secuencial(asistentes),
            cedula,
            nombres,
            apellidos,
            correo,
            direccion,
            True
        )

        # Guardar asistente
        self.repo.guardar("asistentes", asistente.convertir_a_diccionario())

        print("Asistente registrado correctamente.")

    # Metodo para listar asistentes
    def listar(self):
        print("\n--- LISTADO DE ASISTENTES ---")

        asistentes = self.repo.listar("asistentes")

        if len(asistentes) == 0:
            print("No existen asistentes registrados.")
            return

        for asistente in asistentes:
            print(
                f"ID: {asistente['id']} | "
                f"Cédula: {asistente['cedula']} | "
                f"Nombres: {asistente['nombres']} {asistente['apellidos']} | "
                f"Correo: {asistente['correo']} | "
                f"Direccion: {asistente['direccion']}"
            )

    # Metodo para modificar asistentes
    def modificar(self):
        print("\n--- MODIFICAR ASISTENTE ---")

        while True:
            id_asistente = pedir_entero("Ingrese el ID del asistente a modificar: ")

            asistente = self.repo.buscar_por_id("asistentes", id_asistente)

            if asistente is None:
                print("Error. No existe un asistente activo con ese ID.")
                continue

            break
        
        print("Deje vacío un campo si no desea modificarlo.")
        
        while True:
            nueva_cedula = input(f"Cédula actual ({asistente['cedula']}): ").strip()

            if nueva_cedula == "":
                nueva_cedula = asistente["cedula"]
                break

            if not validar_cedula_ecuatoriana(nueva_cedula):
                print("Error. La cédula ecuatoriana no es válida.")
                continue

            existente = self.repo.buscar_por_campo(
                "asistentes",
                "cedula",
                nueva_cedula
            )

            if (existente and existente["id"] != id_asistente):
                print("Ya existe un asistente con esa cédula.")
                continue

            break

        while True:
            nuevos_nombres = input(f"Nombres actuales ({asistente['nombres']}): ").strip()

            if nuevos_nombres == "":
                nuevos_nombres = asistente["nombres"]
                break

            if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+",nuevos_nombres):
                print("Error. Los nombres solo pueden contener letras.")
                continue

            break

        while True:
            nuevos_apellidos = input(f"Apellidos actuales ({asistente['apellidos']}): ").strip()

            if nuevos_apellidos == "":
                nuevos_apellidos = asistente["apellidos"]
                break

            if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+",nuevos_apellidos):
                print("Error. Los apellidos solo pueden contener letras.")
                continue

            break

        while True:
            nuevo_correo = input(f"Correo actual ({asistente['correo']}): ").strip()

            if nuevo_correo == "":
                nuevo_correo = asistente["correo"]
                break

            if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$", nuevo_correo):
                print("Error. El correo no es válido.")
                continue
            
            existente = self.repo.buscar_por_campo(
                "asistentes",
                "correo",
                nuevo_correo
            )

            if (existente and existente["id"] != id_asistente):
                print("Ya existe un asistente con ese correo.")
                continue

            break

        while True:
            nuevo_direccion = input(f"Dirección actual ({asistente['direccion']}): ").strip()

            if nuevo_direccion == "":
                nuevo_direccion = asistente["direccion"]
                break

            if not re.fullmatch(r"[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s.,#\-]+",nuevo_direccion):
                print("Error. La dirección solo puede contener letras y números.")
                continue

            if nuevo_direccion.isdigit():
                print("Error. La dirección no puede contener solo números.")
                continue

            break

        nuevos_datos = {
            "cedula": nueva_cedula,
            "nombres": nuevos_nombres,
            "apellidos": nuevos_apellidos,
            "correo": nuevo_correo,
            "direccion": nuevo_direccion,
            "estado": True
        }

        self.repo.actualizar(
            "asistentes",
            id_asistente,
            nuevos_datos
        )

        print("Asistente modificado correctamente.")

    # Metodo para eliminar asistentes
    def eliminar(self):
        print("\n--- ELIMINAR ASISTENTE ---")

        id_asistente = pedir_entero("Ingrese el ID del asistente a eliminar: ")

        eliminado = self.repo.eliminar_logico("asistentes", id_asistente)

        if eliminado:
            print("Asistente eliminado lógicamente.")
        else:
            print("No se encontró el asistente.")