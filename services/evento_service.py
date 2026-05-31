from models.evento import Evento
from utils.generador_id import generar_id_secuencial
from utils.validaciones import pedir_solo_letras, pedir_fecha, pedir_entero

class EventoService:

    # Constructor de la clase
    def __init__(self, repo):
        self.repo = repo

    # =====================================================================
    # C - CREAR (Registrar Evento)
    # =====================================================================
    def registrar(self):
        print("\n--- REGISTRAR EVENTO ---")

        while True:
            # Quitamos los dos puntos manuales delegando el formato a validaciones.py
            nombre = pedir_solo_letras("Nombre del evento")
            existente = self.repo.buscar_por_campo("eventos", "nombre", nombre)
            if existente:
                print("[❌ ERROR] Ya existe un evento activo con ese nombre. Ingrese otro.")
                continue
            break
        
        ciudad = pedir_solo_letras("Ciudad")
        fecha = pedir_fecha("Fecha del evento")

        # -----------------------------------------------------------------
        # ASIGNACIÓN DE ORGANIZADOR
        # -----------------------------------------------------------------
        organizadores = self.repo.listar("organizadores")
        if len(organizadores) == 0:
            print("[❌ ERROR] No existen organizadores registrados. Debe crear uno primero.")
            return

        print("\n--- ORGANIZADORES DISPONIBLES ---")
        for organizador in organizadores:
            print(f"ID: {organizador['id']} | Nombre: {organizador['nombres']} {organizador['apellidos']} | Correo: {organizador['correo']}")

        while True:
            organizador_id = pedir_entero("Seleccione el ID del organizador o 0 para cancelar")

            if organizador_id == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            organizador = self.repo.buscar_por_id("organizadores", organizador_id)
            
            if organizador is None:
                print("[❌ ERROR] El organizador seleccionado no existe.\n")
                continue
            break

        # -----------------------------------------------------------------
        # ASIGNACIÓN DE VENUE (LUGAR)
        # -----------------------------------------------------------------
        venues = self.repo.listar("venues")
        if len(venues) == 0:
            print("[❌ ERROR] No existen venues registrados. Debe crear uno primero.")
            return

        print("\n--- VENUES DISPONIBLES ---")
        for venue in venues:
            print(f"ID: {venue['id']} | Nombre: {venue['nombre']} | Ciudad: {venue['ciudad']} | Capacidad: {venue['capacidad_maxima']}")

        while True:
            venue_id = pedir_entero("Seleccione el ID del venue o 0 para cancelar")

            if venue_id == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            venue = self.repo.buscar_por_id("venues", venue_id)
            if venue is None:
                print("[❌ ERROR] El venue seleccionado no existe.\n")
                continue

            # Regla de negocio: El lugar debe ser de la misma ciudad del evento
            if venue["ciudad"].lower() != ciudad.lower():
                print("[❌ ERROR] No se pudo registrar: el venue no pertenece a la misma ciudad del evento.\n")
                continue
            break
        
        # -----------------------------------------------------------------
        # ASIGNACIÓN DE PATROCINADORES (Varios IDs separados por coma)
        # -----------------------------------------------------------------
        patrocinadores = self.repo.listar("patrocinadores")
        patrocinadores_ids = []

        if len(patrocinadores) > 0:
            print("\n--- PATROCINADORES DISPONIBLES ---")
            for patrocinador in patrocinadores:
                print(f"ID: {patrocinador['id']} | Empresa: {patrocinador['empresa']} | Aporte: ${patrocinador['aporte']}")

            ids = input("Ingrese IDs de patrocinadores separados por coma (Enter para ninguno): ").strip()
            if ids != "":
                lista_ids = ids.split(",")
                for id_texto in lista_ids:
                    if id_texto.strip() == "":
                        continue
                    try:
                        id_pat = int(id_texto.strip())
                        patrocinador = self.repo.buscar_por_id("patrocinadores", id_pat)
                        if patrocinador:
                            if id_pat not in patrocinadores_ids:
                                patrocinadores_ids.append(id_pat)
                            else:
                                print(f"[ℹ INFO] El patrocinador ID {id_pat} ya fue agregado anteriormente.")
                        else:
                            print(f"[❌ ERROR] El patrocinador con ID {id_pat} no existe.")
                    except ValueError:
                        print(f"[❌ ERROR] '{id_texto.strip()}' no es un número de ID válido.")
                        
        if len(patrocinadores_ids) == 0:
            print("[❌ ERROR] Registro denegado: Debe seleccionar al menos un patrocinador para el evento.")
            return
        
        # La capacidad del evento se hereda automáticamente del Venue elegido
        capacidad_maxima = venue["capacidad_maxima"]
        eventos = self.repo.listar("eventos", solo_activos=False)

        evento = Evento(
            generar_id_secuencial(eventos),
            nombre,
            ciudad,
            fecha,
            capacidad_maxima,
            organizador_id,
            venue_id,
            patrocinadores_ids,
            True
        )

        self.repo.guardar("eventos", evento.convertir_a_diccionario())
        print("[✔ ÉXITO] Evento registrado y configurado correctamente.")

    # =====================================================================
    # R - LEER (Listar Eventos)
    # =====================================================================
    def listar(self):
        print("\n--- LISTADO DE EVENTOS ---")
        eventos = self.repo.listar("eventos")

        if len(eventos) == 0:
            print("[ℹ INFO] No existen eventos activos registrados.")
            return

        for evento in eventos:
            organizador = self.repo.buscar_por_id("organizadores", evento["organizador_id"])
            venue = self.repo.buscar_por_id("venues", evento["venue_id"])

            nombre_organizador = f"{organizador['nombres']} {organizador['apellidos']}" if organizador else "No encontrado"
            nombre_venue = venue["nombre"] if venue else "No encontrado"
            
            empresas = []
            for id_pat in evento.get("patrocinadores_ids", []):
                patrocinador = self.repo.buscar_por_id("patrocinadores", id_pat)
                if patrocinador:
                    empresas.append(patrocinador["empresa"])
            patrocinadores_texto = ", ".join(empresas) if empresas else "Ninguno"

            print(
                f"ID: {evento['id']} | "
                f"Nombre: {evento['nombre']} | "
                f"Ciudad: {evento['ciudad']} | "
                f"Fecha: {evento['fecha']} | "
                f"Aforo Max: {evento['capacidad_maxima']} | "
                f"Organizador: {nombre_organizador} | "
                f"Venue: {nombre_venue} | "
                f"Patrocinadores: {patrocinadores_texto}"
            )

    # =====================================================================
    # U - ACTUALIZAR (Modificar Evento - Versión Segura y Consistente)
    # =====================================================================
    def modificar(self):
        print("\n--- MODIFICAR EVENTO ---")
        
        # 🔄 BUCLE 1: Reintenta hasta que el usuario ingrese un ID de evento real y existente
        while True:
            id_evento = pedir_entero("Ingrese el ID del evento a modificar o 0 para cancelar")

            if id_evento == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            evento = self.repo.buscar_por_id("eventos", id_evento)

            if evento is None:
                print(f"[❌ ERROR] No existe un evento activo con el ID {id_evento}.")
                print("Por favor, verifique e intente con un ID válido de la lista.\n")
                continue

            break

        print("Deje vacío un campo si no desea modificarlo (Presione Enter).")

        # 1. Modificación del Nombre (Controlando que siga siendo único)
        while True:
            nuevo_nombre = pedir_solo_letras("Nombre nuevo", valor_actual=evento['nombre'])
            if nuevo_nombre == evento['nombre']:
                break
            existente = self.repo.buscar_por_campo("eventos", "nombre", nuevo_nombre)
            if existente and existente["id"] != id_evento:
                print("[❌ ERROR] Ya existe otro evento registrado con ese nombre.")
                continue
            break

        # 2. Modificación de la Fecha (Cumpliendo la regla cronológica de 2026+)
        nueva_fecha = pedir_fecha("Fecha nueva", valor_actual=evento['fecha'])

        # Preparamos los datos MANTENIENDO todas las relaciones estructurales intactas
        nuevos_datos = {
            "nombre": nuevo_nombre,
            "ciudad": evento["ciudad"],  
            "fecha": nueva_fecha,
            "capacidad_maxima": evento["capacidad_maxima"],
            "organizador_id": evento["organizador_id"],
            "venue_id": evento["venue_id"],
            "patrocinadores_ids": evento.get("patrocinadores_ids", []),
            "estado": True
        }

        self.repo.actualizar("eventos", id_evento, nuevos_datos)
        print("[✔ ÉXITO] Evento modificado manteniendo de forma consistente sus relaciones.")

    # =====================================================================
    # D - ELIMINAR (Eliminar Evento Lógico - CON REINTENTOS)
    # =====================================================================
    def eliminar(self):
        print("\n--- ELIMINAR EVENTO ---")
        
        # 🔄 BUCLE 2: Reintenta hasta obtener un ID válido para eliminar lógicamente
        while True:
            id_evento = pedir_entero("Ingrese el ID del evento a eliminar o 0 para cancelar")

            if id_evento == 0:
                print("[ℹ INFO] Operación cancelada.")
                return
            
            evento = self.repo.buscar_por_id("eventos", id_evento)

            if evento is None:
                print(f"[❌ ERROR] No existe un evento activo con el ID {id_evento}.")
                print("Por favor, intente con otro ID de la lista.\n")
                continue

            # Regla de negocio: No borrar eventos que ya vendieron entradas
            entradas = self.repo.listar("entradas")
            for entrada in entradas:
                if entrada["evento_id"] == id_evento and entrada["estado"]:
                    print("[❌ ERROR] Denegado: No puede eliminar un evento que ya posee entradas emitidas.")
                    return

            eliminado = self.repo.eliminar_logico("eventos", id_evento)
            if eliminado:
                print("[✔ ÉXITO] Evento eliminado lógicamente.")
                break
            else:
                print(f"[❌ ERROR] No se encontró el evento con el ID {id_evento} o ya está inactivo.")
                print("Por favor, intente con otro ID de la lista.\n")
                continue

    # =====================================================================
    # OP ADICIONAL: Ingresos Totales Por Evento
    # =====================================================================
    def ingresos_por_evento(self):
        print("\n--- REPORTE DE INGRESOS POR EVENTO ---")
        eventos = self.repo.listar("eventos")

        if not eventos:
            print("[ℹ INFO] No existen eventos para procesar ingresos.")
            return

        for evento in eventos:
            entradas = self.repo.listar("entradas")
            total_entradas = sum(entrada["precio"] for entrada in entradas if entrada["evento_id"] == evento["id"])

            patrocinio_total = 0
            for id_pat in evento.get("patrocinadores_ids", []):
                patrocinador = self.repo.buscar_por_id("patrocinadores", id_pat)
                if patrocinador:
                    patrocinio_total += patrocinador["aporte"]

            total = total_entradas + patrocinio_total
            print(
                f"Evento: {evento['nombre']} | "
                f"Entradas: ${total_entradas} | "
                f"Patrocinios: ${patrocinio_total} | "
                f"TOTAL GENERADO: ${total}"
            )

    # =====================================================================
    # OP ADICIONAL: Filtrar Colección por Criterios (Versión Amigable)
    # =====================================================================
    def filtrar_eventos(self):
        print("\n--- FILTRAR EVENTOS ---")
        print("1. Por ciudad")
        print("2. Por rango de fechas")
        opcion = pedir_entero("Seleccione una opción de filtrado")

        # Cambiado a False para forzar la lectura completa de db.json en las pruebas
        eventos = self.repo.listar("eventos")
        if not eventos:
            print("[ℹ INFO] No existen eventos registrados en el sistema.")
            return

        # -----------------------------------------------------------------
        # 🏙️ OPCIÓN 1: FILTRADO POR CIUDAD (CON REINTENTO INTERACTIVO)
        # -----------------------------------------------------------------
        if opcion == 1:
            print("\n--- BUSCAR EVENTOS POR CIUDAD ---")
            print("Deje vacío el campo y presione Enter si desea regresar.")
            
            while True:
                ciudad = pedir_solo_letras("Ingrese la ciudad a buscar", permitir_vacio=True)
                
                if ciudad == "":
                    print("[ℹ INFO] Búsqueda cancelada.")
                    return

                filtrados = [e for e in eventos if e["ciudad"].lower() == ciudad.lower()]
                
                if not filtrados:
                    print(f"[❌ ERROR] No se encontraron eventos registrados en la ciudad de '{ciudad}'.")
                    print("Por favor, intente con otra ciudad o presione Enter para salir.\n")
                    continue
                
                break

        # -----------------------------------------------------------------
        # 📅 OPCIÓN 2: FILTRADO POR RANGO DE FECHAS (TOTALMENTE CORREGIDO)
        # -----------------------------------------------------------------
        elif opcion == 2:
            from datetime import datetime

            print("\n--- BUSCAR EVENTOS POR RANGO DE FECHAS ---")
            
            str_inicio = pedir_fecha("Ingrese la fecha de inicio")
            str_fin = pedir_fecha("Ingrese la fecha de fin")

            def parsear_fecha(fecha_str):
                try:
                    return datetime.strptime(fecha_str, "%d/%m/%Y")
                except ValueError:
                    try:
                        # Procesa perfectamente ingresos flexibles como '1/1/2026'
                        partes = fecha_str.split("/")
                        d = int(partes[0])
                        m = int(partes[1])
                        a = int(partes[2])
                        return datetime(a, m, d)
                    except (ValueError, IndexError):  # Corregido con E mayúscula
                        return None

            f_inicio = parsear_fecha(str_inicio)
            f_fin = parsear_fecha(str_fin)

            if not f_inicio or not f_fin:
                print("[❌ ERROR] Hubo un problema al interpretar las fechas ingresadas.")
                return

            filtrados = []
            for e in eventos:
                fecha_evento = parsear_fecha(e["fecha"])
                if fecha_evento:
                    if f_inicio <= fecha_evento <= f_fin:
                        filtrados.append(e)
            
            if not filtrados:
                print("[ℹ INFO] No se encontraron eventos en el rango de fechas ingresado.")
                return
        
        else:
            print("[❌ ERROR] Opción de filtrado no válida.")
            return

        # -----------------------------------------------------------------
        # 📊 IMPRESIÓN GLOBAL DE RESULTADOS
        # -----------------------------------------------------------------
        print("\n--- RESULTADOS DEL FILTRADO ---")
        for e in filtrados:
            print(f"ID: {e['id']} | Nombre: {e['nombre']} | Ciudad: {e['ciudad']} | Fecha: {e['fecha']} | Aforo: {e['capacidad_maxima']}")