import re

# =====================================================================
# FUNCIÓN AUXILIAR DE CONTROL
# =====================================================================
def campo_vacio(valor):
    return valor is None or str(valor).strip() == ""


# =====================================================================
# VALIDACIÓN: SOLO LETRAS Y ESPACIOS (Nombres, Apellidos, Ciudades)
# =====================================================================
def pedir_solo_letras(mensaje, valor_actual=None, permitir_vacio=False):
    while True:
        # ESTÁNDAR LIMPIO: Añade los dos puntos de forma automática en ambos casos
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else f"{mensaje.strip()}: "
        valor = input(prompt).strip()

        # Si el usuario presiona Enter para modificar, conserva el valor
        if valor == "" and valor_actual is not None:
            return valor_actual

        # Si permitimos vacíos (como en las búsquedas para salir), retornamos el vacío
        if valor == "" and permitir_vacio:
            return valor

        # Validación estándar de obligatoriedad
        if campo_vacio(valor):
            print("[❌ ERROR] Este campo es obligatorio y no puede estar vacío.")
            continue

        # Validación para verificar que sean solo letras y espacios
        if not valor.replace(" ", "").isalpha():
            print("[❌ ERROR] Entrada inválida. Solo se permiten letras.")
            continue

        return valor


# =====================================================================
# VALIDACIÓN: TEXTO ALFANUMÉRICO (Direcciones, Lugares)
# =====================================================================
def pedir_alfanumerico(mensaje, valor_actual=None):
    while True:
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else mensaje
        valor = input(prompt).strip()

        if valor == "" and valor_actual is not None:
            return valor_actual

        if campo_vacio(valor):
            print("[❌ ERROR] Este campo es obligatorio y no puede estar vacío.")
            continue

        if not re.fullmatch(r"[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s.,#\-]+", valor):
            print("[❌ ERROR] Entrada inválida. Solo se permiten letras y números.")
            continue

        if valor.isdigit():
            print("[❌ ERROR] No puede ingresar únicamente números.")
            continue

        return valor


# =====================================================================
# VALIDACIÓN: NOMBRE DE EMPRESA (Patrocinadores)
# =====================================================================
def pedir_empresa(mensaje, valor_actual=None):
    while True:
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else mensaje
        valor = input(prompt).strip()

        if valor == "" and valor_actual is not None:
            return valor_actual

        if campo_vacio(valor):
            print("[❌ ERROR] Este campo es obligatorio y no puede estar vacío.")
            continue

        if not re.fullmatch(r"[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s.,&+_/'’()-]+", valor):
            print("[❌ ERROR] Nombre de empresa inválido.")
            continue

        if not re.search(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ]", valor):
            print("[❌ ERROR] La empresa debe contener al menos una letra.")
            continue

        return valor


# =====================================================================
# VALIDACIÓN: TELÉFONO CELULAR (Exactamente 10 dígitos)
# =====================================================================
def pedir_telefono(mensaje, valor_actual=None):
    while True:
        # CORREGIDO: Estandarizado con el resto de la arquitectura
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else f"{mensaje.strip()}: "
        telefono = input(prompt).strip()

        if telefono == "" and valor_actual is not None:
            return valor_actual

        if campo_vacio(telefono):
            print("[❌ ERROR] El teléfono es un campo requerido.")
            continue

        if not telefono.isdigit():
            print("[❌ ERROR] El teléfono solo debe contener números.")
            continue

        if len(telefono) != 10:
            print("[❌ ERROR] El teléfono debe tener exactamente 10 dígitos.")
            continue

        return telefono


# =====================================================================
# VALIDACIÓN: CORREO ELECTRÓNICO (Formato y Unicidad Inteligente)
# =====================================================================
def pedir_correo(mensaje, valor_actual=None, repo=None, coleccion=None, id_registro=None):
    while True:
        # CORREGIDO: Unificado para evitar textos pegados o duplicados
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else f"{mensaje.strip()}: "
        correo = input(prompt).strip()

        if correo == "" and valor_actual is not None:
            return valor_actual

        if campo_vacio(correo):
            print("[❌ ERROR] El correo electrónico no puede estar vacío.")
            continue

        patron = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
        if not re.fullmatch(patron, correo):
            print("[❌ ERROR] Ingrese un formato de correo válido (ejemplo@dominio.com).")
            continue

        if repo and coleccion:
            existente = repo.buscar_por_campo(coleccion, "correo", correo)
            if existente and (id_registro is None or existente.get("id") != id_registro):
                print(f"[❌ ERROR] El correo '{correo}' ya está registrado por otro usuario.")
                continue

        return correo


# =====================================================================
# VALIDACIÓN: NÚMEROS ENTEROS
# =====================================================================
def pedir_entero(mensaje, valor_actual=None):
    while True:
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else f"{mensaje.strip()}: "
        valor = input(prompt).strip()

        if valor == "" and valor_actual is not None:
            return int(valor_actual)

        if campo_vacio(valor):
            print("[❌ ERROR] Debe ingresar un número entero.")
            continue

        if not valor.isdigit():
            print("[❌ ERROR] Entrada inválida. Solo se permiten números enteros.")
            continue

        return int(valor)


# =====================================================
# VALIDAR ENTERO POSITIVO GENÉRICO
# =====================================================
def pedir_entero_positivo(mensaje, valor_actual=None):
    while True:
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else mensaje
        valor = input(prompt).strip()

        if valor == "" and valor_actual is not None:
            return int(valor_actual)

        if campo_vacio(valor):
            print("[❌ ERROR] Este campo es obligatorio.")
            continue

        if not valor.isdigit():
            print("[❌ ERROR] Entrada inválida. Solo se permiten números enteros puros.")
            continue

        num = int(valor)
        if num <= 0:
            print("[❌ ERROR] El valor debe ser un número entero mayor a cero.")
            continue

        return num


# =====================================================
# VALIDAR CAPACIDAD MÁXIMA DEL VENUE
# =====================================================
def pedir_capacidad_venue(mensaje, valor_actual=None):
    while True:
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else mensaje
        valor = input(prompt).strip()

        if valor == "" and valor_actual is not None:
            return int(valor_actual)

        if campo_vacio(valor):
            print("[❌ ERROR] Este campo es obligatorio.")
            continue

        if not valor.isdigit():
            print("[❌ ERROR] Entrada inválida. Solo se permiten números enteros.")
            continue

        num = int(valor)
        if num < 100:
            print("[❌ ERROR] Capacidad inválida. Un venue debe tener una capacidad mínima de 100 personas.")
            continue

        return num


# =====================================================
# VALIDAR APORTE ECONÓMICO DEL PATROCINADOR
# =====================================================
def pedir_aporte_economico(mensaje, valor_actual=None):
    while True:
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else mensaje
        valor = input(prompt).strip()

        if valor == "" and valor_actual is not None:
            return int(valor_actual)

        if campo_vacio(valor):
            print("[❌ ERROR] El aporte económico es obligatorio.")
            continue

        if not valor.isdigit():
            print("[❌ ERROR] Entrada inválida. Solo se permiten números enteros sin decimales.")
            continue

        num = int(valor)
        if num < 10000:
            print("[❌ ERROR] Monto inválido. El aporte mínimo de un patrocinador debe ser de $10000.")
            continue

        return num


# =====================================================================
# VALIDACIÓN: EDAD (Entre 20 y 100)
# =====================================================================
def pedir_edad(mensaje, valor_actual=None):
    while True:
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else mensaje
        valor = input(prompt).strip()

        if valor == "" and valor_actual is not None:
            return int(valor_actual)

        if campo_vacio(valor):
            print("[❌ ERROR] La edad es obligatoria.")
            continue

        if not valor.isdigit():
            print("[❌ ERROR] La edad solo debe contener números.")
            continue

        edad = int(valor)
        if edad < 20 or edad > 100:
            print("[❌ ERROR] La edad debe estar en el rango de 20 a 100 años.")
            continue

        return edad


# =====================================================================
# VALIDAR FECHA (UNIFICADA Y CORREGIDA: Acepta d/m/yyyy y dd/mm/yyyy)
# =====================================================================
def pedir_fecha(mensaje, valor_actual=None):
    while True:
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else f"{mensaje.strip()}: "
        fecha = input(prompt).strip()

        if fecha == "" and valor_actual is not None:
            return valor_actual

        if campo_vacio(fecha):
            print("[❌ ERROR] La fecha es obligatoria y no puede estar vacía.")
            continue

        # Expresión elástica: permite 1 o 2 dígitos para día y mes, obligatoriamente con barras '/'
        patron = r"^(\d{1,2})/(\d{1,2})/(\d{4})$"
        resultado = re.match(patron, fecha)

        if not resultado:
            print("[❌ ERROR] Formato inválido. Debe usar barras estrictamente (dd/mm/yyyy).")
            continue

        dia = int(resultado.group(1))
        mes = int(resultado.group(2))
        anio = int(resultado.group(3))

        if mes < 1 or mes > 12:
            print("[❌ ERROR] Mes inválido (debe estar entre 1 y 12).")
            continue

        if dia < 1 or dia > 31:
            print("[❌ ERROR] Día inválido para el calendario.")
            continue

        if anio < 2026:
            print("[❌ ERROR] El año ingresado debe ser 2026 o superior.")
            continue

        return fecha


# =====================================================================
# VALIDACIÓN ALGORÍTMICA: CÉDULA ECUATORIANA
# =====================================================================
def validar_cedula_ecuatoriana(cedula):
    if len(cedula) != 10 or not cedula.isdigit():
        return False

    provincia = int(cedula[:2])
    if provincia < 1 or provincia > 24:
        return False

    tercer_digito = int(cedula[2])
    if tercer_digito >= 6:
        return False

    suma = 0
    for i in range(9):
        numero = int(cedula[i])
        if i % 2 == 0:
            numero *= 2
            if numero > 9:
                numero -= 9
        suma += numero

    digito_verificador = (10 - (suma % 10)) % 10
    return digito_verificador == int(cedula[9])


# =====================================================================
# VALIDACIÓN: CONTROL DE ENTRADA DE CÉDULA Y UNICIDAD
# =====================================================================
def pedir_cedula(mensaje, valor_actual=None, repo=None, coleccion=None, id_registro=None):
    while True:
        # CORREGIDO: Ahora el else también tiene los dos puntos automáticos de forma simétrica
        prompt = f"{mensaje.strip()} ({valor_actual}): " if valor_actual is not None else f"{mensaje.strip()}: "
        cedula = input(prompt).strip()

        if cedula == "" and valor_actual is not None:
            return valor_actual

        if campo_vacio(cedula):
            print("[❌ ERROR] La cédula es un campo requerido.")
            continue

        if not validar_cedula_ecuatoriana(cedula):
            print("[❌ ERROR] La cédula ingresada no es una cédula ecuatoriana válida.")
            continue

        if repo and coleccion:
            existente = repo.buscar_por_campo(coleccion, "cedula", cedula)
            if existente and (id_registro is None or existente.get("id") != id_registro):
                print("[❌ ERROR] Ya existe un registro activo con este número de cédula.")
                continue

        return cedula


# =====================================================================
# VALIDACIÓN: CONTROL DE CÓDIGOS DE TICKETS ÚNICOS
# =====================================================================
def validar_codigo_unico(repo, coleccion, campo, valor):
    existente = repo.buscar_por_campo(coleccion, campo, valor)
    return existente is None