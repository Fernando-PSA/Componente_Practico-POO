BLOQUE 1 — Errores de Validación de Campos (utils/validaciones.py)
V-01 · CRÍTICO — pedir_fecha: Fechas inexistentes en el calendario son aceptadas
Archivo: utils/validaciones.py:306-317

La función valida que el día esté entre 1–31 y el mes entre 1–12, pero no usa datetime para verificar si la fecha existe realmente. Ejemplos que el sistema acepta sin error:

31/02/2026 (febrero tiene máximo 29 días)
31/04/2026 (abril tiene máximo 30 días)
29/02/2027 (2027 no es año bisiesto)
31/06/2026, 31/09/2026
V-02 · MEDIO — pedir_telefono: No valida el prefijo de celular ecuatoriano
Archivo: utils/validaciones.py:108-116

Solo valida que sean 10 dígitos. Acepta números como 1234567890 o 0000000000. Los celulares ecuatorianos deben comenzar con 09 (Claro, Movistar, CNT). Un teléfono fijo sería 02, 03, etc., pero estos tienen 9 dígitos totales, no 10.

V-03 · MEDIO — pedir_correo: La unicidad solo busca en registros activos
Archivo: utils/validaciones.py:140-144

buscar_por_campo usa solo_activos=True por defecto. Si un organizador fue eliminado lógicamente y otro nuevo quiere usar el mismo correo, el sistema lo permite, generando duplicados lógicos en la base de datos.

V-04 · MEDIO — pedir_cedula: Misma cédula puede existir en diferentes colecciones
Archivo: utils/validaciones.py:369-373

La unicidad de cédula se valida solo dentro de la misma colección (organizadores o asistentes). Una persona con la misma cédula puede estar registrada como organizador y como asistente simultáneamente. Dependiendo de la regla de negocio, esto es un error.

V-05 · BAJO — pedir_solo_letras: Sin validación de longitud mínima ni máxima
Archivo: utils/validaciones.py:33-37

Un nombre como "A" o una cadena de 5.000 caracteres son aceptados. Tampoco hay normalización de mayúsculas, por lo que "JUAN" y "juan" se almacenan como valores diferentes.

V-06 · BAJO — pedir_aporte_economico y pedir_capacidad_venue: No aceptan decimales
Archivo: utils/validaciones.py:238-244 | utils/validaciones.py:212-218

Ambas usan .isdigit(), por lo que un aporte como $15000.50 o $10500.75 es rechazado. Esto puede ser intencional, pero no está documentado y podría sorprender al usuario.

V-07 · BAJO — validar_codigo_unico está definida pero nunca se invoca
Archivo: utils/validaciones.py:381-383

La función validar_codigo_unico existe como utilidad, pero el generador de códigos en entrada_service.py (línea 87) construye TICK-{evento_id}-{nuevo_id} sin llamarla. Código muerto.

BLOQUE 2 — Errores Lógicos de Negocio (Services + Repository)
L-01 · CRÍTICO — evento_service.modificar(): Solo permite cambiar nombre y fecha
Archivo: services/evento_service.py:213-225

La operación de modificación hardcodea ciudad, organizador_id, venue_id, y patrocinadores_ids con sus valores originales. El usuario no puede corregir un evento asignado al organizador equivocado, ni cambiar el venue, ni agregar/quitar patrocinadores después de creado. Si el evento fue registrado con datos incorrectos en esos campos, la única solución es eliminar y volver a crear.

L-02 · CRÍTICO — venue_service.modificar(): Cambiar la ciudad del venue rompe consistencia con sus eventos
Archivo: services/venue_service.py:92-105

Si un venue tiene eventos activos asignados y se le cambia la ciudad, los eventos quedan con su ciudad original pero el venue apunta a otra ciudad. El sistema no verifica esta dependencia antes de aplicar el cambio, violando la regla de negocio "venue y evento deben ser de la misma ciudad".

L-03 · CRÍTICO — venue_service.modificar(): Reducir capacidad no verifica entradas ya vendidas
Archivo: services/venue_service.py:95

Si un venue tiene 1.000 cupos y se vendieron 800 entradas para un evento asignado a ese venue, el sistema permite reducir la capacidad a 500 sin advertencia. Aunque el evento mantiene su propia capacidad_maxima, el dato del venue queda inconsistente con la realidad operativa.

L-04 · ALTO — entrada_service.registrar(): Un mismo asistente puede comprar múltiples entradas para el mismo evento
Archivo: services/entrada_service.py:66-103

No existe validación que impida que un asistente tenga más de una entrada activa para el mismo evento. Un operador puede, intencional o accidentalmente, emitir 10 entradas para el mismo asistente en el mismo evento, consumiendo cupos que corresponden a otros.

L-05 · ALTO — evento_service.registrar(): Si no existen patrocinadores, el mensaje de error es confuso
Archivo: services/evento_service.py:88-117

Si patrocinadores está vacío (línea 91: if len(patrocinadores) > 0), el sistema salta silenciosamente el bloque de selección y después muestra el error "Registro denegado: debe seleccionar al menos un patrocinador". El usuario no entiende por qué no pudo elegir ninguno — el sistema nunca indicó que no había patrocinadores registrados. Correcto sería verificar primero y mostrar [❌ ERROR] No existen patrocinadores registrados. Cree uno primero. con un return inmediato.

L-06 · ALTO — patrocinador_service.registrar(): No valida unicidad de nombre de empresa
Archivo: services/patrocinador_service.py:25-27

Se pueden registrar dos patrocinadores con exactamente el mismo nombre de empresa. Esto genera duplicados que aparecerán en el listado de selección al registrar eventos, causando confusión operativa.

L-07 · ALTO — venue_service.registrar(): No valida unicidad de nombre de venue
Archivo: services/venue_service.py:24-27

Igual que con patrocinadores: dos venues con el mismo nombre y ciudad pueden coexistir. Al seleccionar venue para un evento, el operador verá entradas duplicadas sin poder distinguirlas.

L-08 · MEDIO — evento_service.filtrar_eventos(): No valida que fecha de inicio sea anterior a fecha de fin
Archivo: services/evento_service.py:340-373

Si el usuario ingresa un rango invertido (inicio = 15/12/2026, fin = 01/01/2026), el sistema no lanza error: simplemente no encuentra eventos y muestra el mensaje informativo de "rango sin resultados". Esto oculta el error real del usuario.

L-09 · MEDIO — evento_service.registrar(): Comparación de nombre de evento es case-sensitive
Archivo: services/evento_service.py:20-23

buscar_por_campo compara strings con str(a) == str(b), sin .lower(). Por tanto "Festival Rock" y "festival rock" se consideran eventos distintos y ambos pueden registrarse.

L-10 · MEDIO — entrada_service.listar_asistentes_ordenada(): No filtra por evento
Archivo: services/entrada_service.py:165-202

El reporte muestra todos los asistentes con entradas activas de todos los eventos combinados. Si hay 5 eventos activos, el reporte mezcla asistentes de todos ellos sin separación. No existe opción para filtrar el reporte por evento específico.

L-11 · MEDIO — asistente_service.eliminar(): Verifica solo entradas activas, ignora historial
Archivo: services/asistente_service.py:141-145

self.repo.listar("entradas") retorna solo estado=True. Si un asistente tiene únicamente entradas canceladas (historial), el sistema permite eliminarlo lógicamente. El registro histórico de que ese asistente alguna vez asistió a un evento se vuelve huérfano (la entrada existe pero el asistente_id referencia a un registro inactivo).

L-12 · BAJO — Ningún flujo de eliminación pide confirmación al usuario
Archivo: Todos los service.eliminar() — ej. services/organizador_service.py:127-151

Una vez que el operador ingresa un ID válido, la eliminación lógica se ejecuta de inmediato sin un paso de confirmación del tipo "¿Confirma eliminar el registro ID X? (s/n)". Un error de tipeo en el ID puede eliminar el registro equivocado.

L-13 · BAJO — entrada_service: No existe opción de modificar una entrada
Archivo: app.py:183-205 | services/entrada_service.py

El menú de entradas ofrece Emitir, Listar, Cancelar y Reporte, pero no Modificar. Si se cometió un error en el precio o en el asistente asignado, la única salida es cancelar la entrada y emitir una nueva.

Resumen de Prioridad
Clave	Severidad	Módulo afectado
L-01	Crítico	evento_service.modificar
L-02	Crítico	venue_service.modificar
L-03	Crítico	venue_service.modificar
V-01	Crítico	pedir_fecha
L-04	Alto	entrada_service.registrar
L-05	Alto	evento_service.registrar
L-06	Alto	patrocinador_service.registrar
L-07	Alto	venue_service.registrar
V-02	Medio	pedir_telefono
V-03	Medio	pedir_correo
L-08	Medio	evento_service.filtrar_eventos
L-09	Medio	evento_service.registrar
L-10	Medio	entrada_service.listar_asistentes_ordenada
L-11	Medio	asistente_service.eliminar
V-04	Medio	pedir_cedula
V-05	Bajo	pedir_solo_letras
V-06	Bajo	pedir_aporte_economico / pedir_capacidad_venue
V-07	Bajo	validar_codigo_unico (código muerto)
L-12	Bajo	Todos los eliminar()
L-13	Bajo	entrada_service
Con este inventario podemos proceder a hacer los cambios en el código. ¿Arrancamos por los críticos o prefieres un orden diferente?