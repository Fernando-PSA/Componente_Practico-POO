import re


# =====================================================
# VALIDAR SI UN CAMPO ESTA VACIO
# =====================================================
def campo_vacio(valor):

    return valor is None or str(valor).strip() == ""


# =====================================================
# VALIDAR SOLO LETRAS Y ESPACIOS
# NO PERMITE:
# numeros
# caracteres especiales
# =====================================================
def pedir_solo_letras(mensaje):

    while True:

        valor = input(mensaje).strip()

        if campo_vacio(valor):
            print(
                "Error. Este campo no puede estar vacío."
            )
            continue

        if not re.fullmatch(
            r"[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+",
            valor
        ):
            print(
                "Error. Solo se permiten letras."
            )
            continue

        return valor


# =====================================================
# VALIDAR TEXTO ALFANUMERICO
# PERMITE:
# letras
# numeros
# espacios
#
# NO PERMITE:
# caracteres especiales
# =====================================================
def pedir_alfanumerico(mensaje):

    while True:

        valor = input(mensaje).strip()

        if campo_vacio(valor):
            print(
                "Error. Este campo no puede estar vacío."
            )
            continue

        if not re.fullmatch(
            r"[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]+",
            valor
        ):
            print(
                "Error. Solo se permiten letras y números."
            )
            continue

        # Evitar SOLO números
        if valor.isdigit():
            print(
                "Error. No puede ingresar únicamente números."
            )
            continue

        return valor

# =====================================================
# VALIDAR EMPRESA
# PERMITE:
# letras
# numeros
# espacios
# algunos caracteres especiales
# =====================================================
# =====================================================
# VALIDAR EMPRESA
# =====================================================
def pedir_empresa(mensaje):

    while True:

        valor = input(mensaje).strip()

        if campo_vacio(valor):

            print(
                "Error. Este campo no puede estar vacío."
            )

            continue

        if not re.fullmatch(
            r"[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s.,&+_/'’()-]+",
            valor
        ):

            print(
                "Error. Nombre de empresa inválido."
            )

            continue

        if not re.search(
            r"[a-zA-ZáéíóúÁÉÍÓÚñÑ]",
            valor
        ):

            print(
                "Error. La empresa debe contener al menos una letra."
            )

            continue

        return valor

# =====================================================
# VALIDAR TELEFONO
# SOLO NUMEROS
# EXACTAMENTE 10 DIGITOS
# =====================================================
def pedir_telefono(mensaje):

    while True:

        telefono = input(mensaje).strip()

        if not telefono.isdigit():

            print(
                "Error. El teléfono solo debe contener números."
            )

            continue

        if len(telefono) != 10:

            print(
                "Error. El teléfono debe tener 10 dígitos."
            )

            continue

        return telefono


# =====================================================
# VALIDAR CORREO
# =====================================================
def pedir_correo(mensaje):

    while True:

        correo = input(mensaje).strip()

        if campo_vacio(correo):

            print(
                "Error. El correo no puede estar vacío."
            )

            continue

        patron = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"

        if not re.fullmatch(patron, correo):

            print(
                "Error. Ingrese un correo válido."
            )

            continue

        return correo


# =====================================================
# VALIDAR ENTERO
# SOLO NUMEROS ENTEROS
# =====================================================
def pedir_entero(mensaje):

    while True:

        valor = input(mensaje).strip()

        if not valor.isdigit():

            print(
                "Error. Solo se permiten números enteros."
            )

            continue

        return int(valor)


# =====================================================
# VALIDAR ENTERO POSITIVO
# =====================================================
def pedir_entero_positivo(mensaje):

    while True:

        valor = pedir_entero(mensaje)

        if valor <= 0:

            print(
                "Error. Debe ingresar un número mayor a cero."
            )

            continue

        return valor


# =====================================================
# VALIDAR EDAD
# ENTRE 20 Y 100
# =====================================================
def pedir_edad(mensaje):

    while True:

        edad = input(mensaje).strip()

        if not edad.isdigit():

            print(
                "Error. La edad solo debe contener números."
            )

            continue

        edad = int(edad)

        if edad < 20 or edad > 100:

            print(
                "Error. La edad debe estar entre 20 y 100 años."
            )

            continue

        return edad


# =====================================================
# VALIDAR FECHA
# FORMATOS:
# dd/mm/yyyy
# dd-mm-yyyy
# =====================================================
def pedir_fecha(mensaje):

    while True:

        fecha = input(mensaje).strip()

        patron = r"^(\d{2})([/\-])(\d{2})\2(\d{4})$"

        resultado = re.match(patron, fecha)

        if not resultado:

            print(
                "Error. Formato inválido. "
                "Use dd/mm/yyyy o dd-mm-yyyy."
            )

            continue

        dia = int(resultado.group(1))
        mes = int(resultado.group(3))
        anio = int(resultado.group(4))

        if dia < 1 or dia > 31:

            print(
                "Error. Día inválido."
            )

            continue

        if mes < 1 or mes > 12:

            print(
                "Error. Mes inválido."
            )

            continue

        if anio < 2026:

            print(
                "Error. El año debe ser 2026 o superior."
            )

            continue

        return fecha
    
def validar_fecha(fecha):

    patron = r"^(\d{1,2})([/\-])(\d{1,2})\2(\d{4})$"

    resultado = re.match(patron, fecha)

    if not resultado:
        return False

    dia = int(resultado.group(1))
    mes = int(resultado.group(3))
    anio = int(resultado.group(4))

    if dia < 1 or dia > 31:
        return False

    if mes < 1 or mes > 12:
        return False

    if anio < 2026:
        return False

    return True


# =====================================================
# VALIDAR CEDULA ECUATORIANA
# =====================================================
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

    digito_verificador = (
        10 - (suma % 10)
    ) % 10

    return digito_verificador == int(cedula[9])


# =====================================================
# PEDIR CEDULA
# =====================================================
def pedir_cedula(mensaje):

    while True:

        cedula = input(mensaje).strip()

        if campo_vacio(cedula):

            print(
                "Error. La cédula no puede estar vacía."
            )

            continue

        if not validar_cedula_ecuatoriana(cedula):

            print(
                "Error. La cédula ecuatoriana no es válida."
            )

            continue

        return cedula


# =====================================================
# VALIDAR CODIGO UNICO
# =====================================================
def validar_codigo_unico(
    repo,
    coleccion,
    campo,
    valor
):

    existente = repo.buscar_por_campo(
        coleccion,
        campo,
        valor
    )

    return existente is None