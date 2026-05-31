from models.entrada import Entrada
from utils.generador_id import generar_id_secuencial
from utils.validaciones import pedir_entero, validar_codigo_unico, pedir_entero_positivo

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
            print(f"ID: {ev['id']} | Nombre: {ev['nombre']} | Ciudad: {ev['ciudad']} | Capacidad Máx:: {ev['capacidad_maxima']} personas")
            
        id_evento = pedir_entero("Seleccione el ID del evento: ")
        evento = self.repo.buscar_por_id("eventos", id_evento)
        if not evento:
            print("[❌ ERROR] El evento seleccionado no existe.")
            return

        # 2. Selección del Asistente
        asistentes = self.repo.listar("asistentes")
        if len(asistentes) == 0:
            print("[❌ ERROR] No hay asistentes registrados.")
            return
            
        print("\n--- ASISTENTES DISPONIBLES ---")
        for asis in asistentes:
            # Usamos 'nombres' y 'apellidos' tal como están en tu db.json y modelo
            print(f"ID: {asis['id']} | Nombre: {asis['nombres']} {asis['apellidos']} | Cédula: {asis['cedula']}")
            
        id_asistente = pedir_entero("Seleccione el ID del asistente: ")
        asistente = self.repo.buscar_por_id("asistentes", id_asistente)
        if not asistente:
            print("[❌ ERROR] El asistente seleccionado no existe.")
            return

        # 3. 🆕 Preguntar CUÁNTAS entradas quiere comprar
        cantidad_tickets = pedir_entero_positivo("¿Cuántas entradas desea comprar para este asistente?: ")

        # 4. Preguntar el valor monetario de cada ticket
        precio = pedir_entero_positivo("Valor en dólares de cada entrada ($): ")

        # Contamos cuántas entradas ya se han vendido históricamente para este evento
        entradas_totales = self.repo.listar("entradas", solo_activos=False)
        entradas_vendidas = sum(1 for e in entradas_totales if e["evento_id"] == id_evento and e["estado"] == True)

        # 🚨 CONTROL DE AFORO ANTES DE PROCESAR: Verificamos si caben todas las solicitadas
        if Stream_Aforo := (entradas_vendidas + cantidad_tickets) > evento["capacidad_maxima"]:
            cupos_disponibles = evento["capacidad_maxima"] - entradas_vendidas
            print(f"[❌ ERROR] Operación bloqueada por Control de Aforo.")
            print(f"[ℹ INFO] Solo quedan {cupos_disponibles} cupos disponibles. No puede comprar {cantidad_tickets}.")
            return

        # 5. Bucle automático para emitir cada ticket individual
        print("\nProcesando emisión de tickets...")
        for i in range(cantidad_tickets):
            # 🔄 CAMBIO AQUÍ: Llamamos al nombre correcto de tu repositorio
            nuevo_id = self.repo.generar_id_secuencial("entradas")
            codigo_ticket = f"TICK-{id_evento}-{nuevo_id}"

            # Instanciamos el modelo de la Entrada
            nueva_entrada = Entrada(
                id=nuevo_id,
                evento_id=id_evento,
                asistente_id=id_asistente,
                codigo=codigo_ticket,
                precio=precio
            )

            # Guardamos físicamente en el JSON
            self.repo.guardar("entradas", nueva_entrada.convertir_a_diccionario())
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
    # D - ELIMINAR (Cancelar/Anular Entrada)
    # =====================================================================
    def eliminar(self):
        print("\n--- CANCELAR ENTRADA ---")
        id_entrada = pedir_entero("Ingrese el ID de registro de la entrada a cancelar: ")

        eliminado = self.repo.eliminar_logico("entradas", id_entrada)
        if eliminado:
            print("[✔ ÉXITO] La entrada ha sido cancelada y el cupo fue liberado correctamente.")
        else:
            print("[❌ ERROR] No se encontró la entrada seleccionada o ya se encontraba inactiva.")

    # =====================================================================
    # OP ADICIONAL: Lista de Asistentes Ordenada (Por Apellido o Código)
    # =====================================================================
    def listar_asistentes_ordenada(self):
        print("\n--- LISTA DE ASISTENTES ORDENADA ---")
        entradas = self.repo.listar("entradas")
        asistentes = self.repo.listar("asistentes")

        if not entradas or not asistentes:
            print("[ℹ INFO] Datos insuficientes en el sistema para generar un ordenamiento.")
            return

        print("\nCriterios de Ordenamiento:")
        print("1. Ordenar Alfabéticamente por Apellido")
        print("2. Ordenar por Código Secuencial de Entrada")
        opcion = pedir_entero("Seleccione una opción: ")

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