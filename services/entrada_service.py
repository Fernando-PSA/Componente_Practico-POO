from models.entrada import Entrada
from utils.generador_id import generar_id_secuencial
from utils.validaciones import pedir_entero, pedir_entero_positivo

class EntradaService:

    # Constructor de la clase
    def __init__(self, repo):
        self.repo = repo

    # =====================================================================
    # C - CREAR / EMITIR ENTRADAS (Soportando Múltiples Tickets por Compra)
    # =====================================================================
    def registrar(self):
        print("\n--- EMITIR ENTRADAS ---")
        
        # 1. Selección del Evento
        eventos = self.repo.listar("eventos")
        if len(eventos) == 0:
            print("[❌ ERROR] No hay eventos registrados.")
            return
            
        print("\n--- EVENTOS DISPONIBLES ---")
        for ev in eventos:
            print(f"ID: {ev['id']} | Nombre: {ev['nombre']} | Ciudad: {ev['ciudad']} | Capacidad Máx: {ev['capacidad_maxima']} personas")
            
        # 🔄 BUCLE 1: Reintenta hasta que el operador ingrese un ID de evento existente
        while True:
            id_evento = pedir_entero("Seleccione el ID del evento o 0 para cancelar")

            if id_evento == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            evento = self.repo.buscar_por_id("eventos", id_evento)
            if not evento:
                print(f"[❌ ERROR] El evento con ID {id_evento} no existe. Por favor, seleccione otro.\n")
                continue
            break

        # 2. Selección del Asistente
        asistentes = self.repo.listar("asistentes")
        if len(asistentes) == 0:
            print("[❌ ERROR] No hay asistentes registrados.")
            return
            
        print("\n--- ASISTENTES DISPONIBLES ---")
        for asis in asistentes:
            print(f"ID: {asis['id']} | Nombre: {asis['nombres']} {asis['apellidos']} | Cédula: {asis['cedula']}")
            
        # 🔄 BUCLE 2: Reintenta hasta que el operador ingrese un ID de asistente existente
        while True:
            id_asistente = pedir_entero("Seleccione el ID del asistente o 0 para cancelar")

            if id_asistente == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            asistente = self.repo.buscar_por_id("asistentes", id_asistente)
            if not asistente:
                print(f"[❌ ERROR] El asistente con ID {id_asistente} no existe. Por favor, seleccione otro.\n")
                continue
            break

        # [L-04] Verifica que el asistente no tenga ya una entrada activa para este evento
        #         para evitar que un mismo asistente consuma múltiples cupos del mismo evento
        entradas_existentes = self.repo.listar("entradas")
        ya_tiene = [e for e in entradas_existentes if e["evento_id"] == id_evento and e["asistente_id"] == id_asistente]
        if ya_tiene:
            print(f"[❌ ERROR] El asistente ya posee {len(ya_tiene)} entrada(s) activa(s) para este evento.")
            return

        # 3. Preguntar cuántas entradas quiere comprar
        cantidad_tickets = pedir_entero_positivo("¿Cuántas entradas desea comprar para este asistente?")

        # 4. Preguntar el valor monetario de cada ticket
        precio = pedir_entero_positivo("Valor en dólares de cada entrada ($)")

        # Contamos cuántas entradas ya se han vendido históricamente para este evento
        entradas_totales = self.repo.listar("entradas", solo_activos=False)
        entradas_vendidas = sum(1 for e in entradas_totales if e["evento_id"] == id_evento and e["estado"] == True)

        # 🚨 CONTROL DE AFORO ANTES DE PROCESAR: Verificamos si caben todas las solicitadas
        if (entradas_vendidas + cantidad_tickets) > evento["capacidad_maxima"]:
            cupos_disponibles = evento["capacidad_maxima"] - entradas_vendidas
            print(f"[❌ ERROR] Operación bloqueada por Control de Aforo.")
            print(f"[ℹ INFO] Solo quedan {cupos_disponibles} cupos disponibles. No puede comprar {cantidad_tickets}.")
            return

        # 5. Bucle automático para emitir cada ticket individual
        print("\nProcesando emisión de tickets...")
        for i in range(cantidad_tickets):
            # Generamos el ID secuencial basado en la lista actualizada en tiempo real
            nuevo_id = generar_id_secuencial(entradas_totales)
            codigo_ticket = f"TICK-{id_evento}-{nuevo_id}"

            # Instanciamos el modelo de la Entrada
            nueva_entrada = Entrada(
                id=nuevo_id,
                evento_id=id_evento,
                asistente_id=id_asistente,
                codigo=codigo_ticket,
                precio=precio
            )

            # Convertimos a diccionario e insertamos en la lista local antes de guardar
            diccionario_entrada = nueva_entrada.convertir_a_diccionario()
            entradas_totales.append(diccionario_entrada)

            # Guardamos físicamente en el JSON
            self.repo.guardar("entradas", diccionario_entrada)
            print(f"   -> [✔] Ticket {i+1}/{cantidad_tickets} generado con código: {codigo_ticket}")

        # Mensaje de éxito global con la matemática correcta en unidades
        entradas_vendidas_actualizadas = entradas_vendidas + cantidad_tickets
        cupos_restantes = evento["capacidad_maxima"] - entradas_vendidas_actualizadas
        
        print(f"\n[✔ COMPRA EXITOSA] Se emitieron {cantidad_tickets} entradas correctamente.")
        print(f"[📊 AFORO ACTUAL] Cupos restantes en el evento: {cupos_restantes}")

    # =====================================================================
    # R - LEER (Listar Entradas Emitidas)
    # =====================================================================
    def listar(self):
        print("\n--- LISTADO DE ENTRADAS EMITIDAS ---")
        entradas = self.repo.listar("entradas")

        if not entradas:
            print("[ℹ INFO] No existen registros de entradas emitidas.")
            return

        for entrada in entradas:
            evento = self.repo.buscar_por_id("eventos", entrada["evento_id"])
            asistente = self.repo.buscar_por_id("asistentes", entrada["asistente_id"])

            nombre_evento = evento["nombre"] if evento else "No encontrado"
            nombre_asistente = f"{asistente['nombres']} {asistente['apellidos']}" if asistente else "No encontrado"

            print(
                f"ID Registro: {entrada['id']} | "
                f"Código Ticket: {entrada['codigo']} | "
                f"Evento: {nombre_evento} | "
                f"Asistente: {nombre_asistente} | "
                f"Precio Pagado: ${entrada['precio']}"
            )

    # =====================================================================
    # D - ELIMINAR (Cancelar/Anular Entrada - VERSIÓN CON REINTENTOS)
    # =====================================================================
    def eliminar(self):
        print("\n--- CANCELAR ENTRADA ---")
        
        # 🔄 BUCLE 3: Reintenta pedir el ID hasta que se ingrese uno que exista en db.json
        while True:
            id_entrada = pedir_entero("Ingrese el ID de registro de la entrada a cancelar o 0 para cancelar")

            if id_entrada == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            entrada_encontrada = self.repo.buscar_por_id("entradas", id_entrada)
            if not entrada_encontrada:
                print(f"[❌ ERROR] No se encontró la entrada con el ID {id_entrada} o ya se encuentra inactiva.")
                print("Por favor, intente con otro ID válido de la lista.\n")
                continue

            # [L-12] Confirmación explícita antes de cancelar la entrada
            confirmacion = input(f"¿Confirma cancelar la entrada con código '{entrada_encontrada['codigo']}'? (s/n): ").strip().lower()
            if confirmacion != "s":
                print("[ℹ INFO] Operación cancelada por el usuario.")
                return

            eliminado = self.repo.eliminar_logico("entradas", id_entrada)
            if eliminado:
                print("[✔ ÉXITO] La entrada ha sido cancelada y el cupo fue liberado correctamente.")
                break
            else:
                print(f"[❌ ERROR] No se encontró la entrada con el ID {id_entrada} o ya se encuentra inactiva.")
                print("Por favor, intente con otro ID válido de la lista.\n")
                continue

    # =====================================================================
    # OP ADICIONAL: Lista de Asistentes Ordenada (Por Apellido o Código)
    # =====================================================================
    def listar_asistentes_ordenada(self):
        """
        [L-10] Reporte de asistentes ordenados filtrado por evento.
        Antes de ordenar, solicita al usuario que seleccione el evento específico
        para evitar mezclar asistentes de diferentes eventos en el mismo reporte.
        """
        print("\n--- LISTA DE ASISTENTES ORDENADA ---")

        # [L-10] Selección de evento específico para filtrar el reporte
        eventos = self.repo.listar("eventos")
        if not eventos:
            print("[ℹ INFO] No hay eventos registrados.")
            return
        print("\n--- EVENTOS DISPONIBLES ---")
        for ev in eventos:
            print(f"ID: {ev['id']} | Nombre: {ev['nombre']} | Ciudad: {ev['ciudad']}")
        while True:
            id_evento_filtro = pedir_entero("Seleccione el ID del evento a consultar o 0 para todos")
            if id_evento_filtro == 0:
                entradas = self.repo.listar("entradas")
                break
            ev_sel = self.repo.buscar_por_id("eventos", id_evento_filtro)
            if not ev_sel:
                print("[❌ ERROR] El evento seleccionado no existe.")
                continue
            entradas = [e for e in self.repo.listar("entradas") if e["evento_id"] == id_evento_filtro]
            break

        asistentes = self.repo.listar("asistentes")

        if not entradas or not asistentes:
            print("[ℹ INFO] Datos insuficientes en el sistema para generar un ordenamiento.")
            return

        print("\nCriterios de Ordenamiento:")
        print("1. Ordenar Alfabéticamente por Apellido")
        print("2. Ordenar por Código Secuencial de Entrada")
        opcion = pedir_entero("Seleccione una opción o 0 para cancelar")

        if opcion == 0:
            print("[ℹ INFO] Operación cancelada.")
            return

        lista_mapeada = []
        for entrada in entradas:
            asistente = self.repo.buscar_por_id("asistentes", entrada["asistente_id"])
            if asistente and entrada["estado"]:
                lista_mapeada.append({
                    "apellido": asistente["apellidos"],
                    "nombre": asistente["nombres"],
                    "codigo": entrada["codigo"]
                })

        if opcion == 1:
            lista_mapeada.sort(key=lambda x: x["apellido"].lower())
        elif opcion == 2:
            lista_mapeada.sort(key=lambda x: x["codigo"])
        else:
            print("[❌ ERROR] Opción de ordenamiento no válida.")
            return

        print("\n--- REPORTE DE ASISTENTES ORDENADOS ---")
        for item in lista_mapeada:
            print(f"Asistente: {item['apellido']}, {item['nombre']} | Código Ticket: {item['codigo']}")

    # =====================================================================
    # U - MODIFICAR (Corregir precio de una entrada existente)
    # =====================================================================
    def modificar(self):
        """
        [L-13] Permite corregir el precio de una entrada ya emitida.
        Sin esta opción el operador debía cancelar y re-emitir la entrada completa,
        generando un nuevo código y consumiendo cupo innecesariamente.
        """
        print("\n--- MODIFICAR ENTRADA ---")

        while True:
            id_entrada = pedir_entero("Ingrese el ID de la entrada a modificar o 0 para cancelar")

            if id_entrada == 0:
                print("[ℹ INFO] Operación cancelada.")
                return

            entrada = self.repo.buscar_por_id("entradas", id_entrada)

            if entrada is None:
                print(f"[❌ ERROR] No existe una entrada activa con el ID {id_entrada}.")
                print("Por favor, verifique e intente con un ID válido de la lista.\n")
                continue
            break

        evento = self.repo.buscar_por_id("eventos", entrada["evento_id"])
        asistente = self.repo.buscar_por_id("asistentes", entrada["asistente_id"])
        nombre_evento = evento["nombre"] if evento else "No encontrado"
        nombre_asistente = f"{asistente['nombres']} {asistente['apellidos']}" if asistente else "No encontrado"

        print(f"\nEntrada seleccionada: Código {entrada['codigo']} | Evento: {nombre_evento} | Asistente: {nombre_asistente}")
        print("Deje vacío si no desea modificar el campo (Presione Enter).")

        nuevo_precio = pedir_entero_positivo(f"Nuevo precio (actual: ${entrada['precio']})")

        nuevos_datos = {
            "codigo": entrada["codigo"],
            "evento_id": entrada["evento_id"],
            "asistente_id": entrada["asistente_id"],
            "precio": nuevo_precio,
            "estado": True
        }

        self.repo.actualizar("entradas", id_entrada, nuevos_datos)
        print("[✔ ÉXITO] Precio de la entrada actualizado correctamente.")