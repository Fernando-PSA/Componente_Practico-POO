import re

from models.organizador import Organizador
from utils.generador_id import generar_id_secuencial
from utils.validaciones import pedir_cedula, pedir_solo_letras, pedir_correo, pedir_telefono, pedir_entero, validar_cedula_ecuatoriana


class OrganizadorService:

    # Constructor de la clase
    def __init__(self, repo):
        self.repo = repo

    # Metodo para registrar un organizador
    def registrar(self):
        print("\n--- REGISTRAR ORGANIZADOR ---")

        while True:
            cedula = pedir_cedula("Cédula: ")

            organizador_existente = self.repo.buscar_por_campo(
                "organizadores",
                "cedula",
                cedula
            )

            if organizador_existente:
                print("Ya existe un organizador activo con esa cédula.")
                continue

            break
        
        nombre = pedir_solo_letras("Nombre del organizador: ")
        
        while True:
            correo = pedir_correo("Correo: ")

            organizador_existente = self.repo.buscar_por_campo(
                "organizadores",
                "correo",
                correo
            )

            if organizador_existente:
                print("Ya existe un organizador activo con ese correo.")
                continue

            break

        telefono = pedir_telefono("Teléfono: ")

        # Obtener todos los organizadores
        organizadores = self.repo.listar("organizadores", solo_activos=False)

        # Crear objeto Organizador
        organizador = Organizador(
            generar_id_secuencial(organizadores),
            cedula,
            nombre,
            correo,
            telefono,
            True
        )

        # Guardar organizador en formato diccionario
        self.repo.guardar("organizadores", organizador.convertir_a_diccionario())
        
        print("Organizador registrado correctamente.")

    # Metodo para listar organizadores
    def listar(self):
        print("\n--- LISTADO DE ORGANIZADORES ---")

        organizadores = self.repo.listar("organizadores")

        if len(organizadores) == 0:
            print("No existen organizadores registrados.")
            return

        for organizador in organizadores:
            print(
                f"ID: {organizador['id']} | "
                f"Cédula: {organizador['cedula']} | "
                f"Nombre: {organizador['nombre']} | "
                f"Correo: {organizador['correo']} | "
                f"Teléfono: {organizador['telefono']}"
            )

    # Metodo para modificar organizadores
    def modificar(self):
        print("\n--- MODIFICAR ORGANIZADOR ---")
        while True:
            id_organizador = pedir_entero("Ingrese el ID del organizador a modificar: ")
            organizador = self.repo.buscar_por_id("organizadores",id_organizador)

            if organizador is None:
                print("Error. No existe un organizador activo con ese ID.")
                continue
            
            break

        print("Deje vacío un campo si no desea modificarlo.")

        while True:
            nueva_cedula = input(f"Cédula actual ({organizador['cedula']}): ").strip()

            if nueva_cedula == "":
                nueva_cedula = organizador["cedula"]
                break

            if not validar_cedula_ecuatoriana(nueva_cedula):
                print("Error. La cédula ecuatoriana no es válida.")
                continue

            existente = self.repo.buscar_por_campo(
                "organizadores",
                "cedula",
                nueva_cedula
            )

            if (existente and existente["id"] != id_organizador):
                print("Ya existe un organizador con esa cédula.")
                continue

            break

        while True:
            nuevo_nombre = input(f"Nombre actual ({organizador['nombre']}): ").strip()

            if nuevo_nombre == "":
                nuevo_nombre = organizador["nombre"]
                break

            if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+", nuevo_nombre):
                print("Error. Solo se permiten letras.")
                continue

            break

        while True:
            nuevo_correo = input(f"Correo actual ({organizador['correo']}): ").strip()

            if nuevo_correo == "":
                nuevo_correo = organizador["correo"]
                break

            if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$", nuevo_correo):
                print("Error. El correo no es válido.")
                continue
            
            existente = self.repo.buscar_por_campo(
                "organizadores",
                "correo",
                nuevo_correo
            )

            if existente and existente["id"] != id_organizador:
                print("Ya existe un organizador con ese correo.")
                continue
            
            break

        while True:
            nuevo_telefono = input(f"Teléfono actual ({organizador['telefono']}): ").strip()

            if nuevo_telefono == "":
                nuevo_telefono = organizador["telefono"]
                break

            if not nuevo_telefono.isdigit():
                print("Error. El teléfono solo debe contener números.")
                continue

            if len(nuevo_telefono) != 10:
                print("Error. El teléfono debe tener 10 dígitos.")
                continue

            break

        nuevos_datos = {
        "cedula": nueva_cedula,
        "nombre": nuevo_nombre,
        "correo": nuevo_correo,
        "telefono": nuevo_telefono,
        "estado": True
        }

        self.repo.actualizar(
            "organizadores",
            id_organizador,
            nuevos_datos
        )

        print("Organizador modificado correctamente.")

    # Metodo para eliminar organizadores
    def eliminar(self):
        print("\n--- ELIMINAR ORGANIZADOR ---")

        id_organizador = pedir_entero(
            "Ingrese el ID del organizador a eliminar: "
        )

        eliminado = self.repo.eliminar_logico(
            "organizadores",
            id_organizador
        )

        if eliminado:
            print("Organizador eliminado lógicamente.")
        else:
            print("No se encontró el organizador.")