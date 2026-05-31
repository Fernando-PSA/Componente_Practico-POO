#Importa el modulo JSON para trabajar con archivos JSON
import json
#Importamos OS para interactuar con el sistema operativo y crear archivos, carpetas, etc
import os

#Se crea la clase RepoJson para gestionar la persistencia de datos en el archivo .json
class RepoJson:
    #Constructor de la clase , en la cual se coloca la ruta por defecto de la carpeta y archivo .json
    def __init__(self, ruta_archivo="data/db.json"):
        #Se guarda la ruta del archivo automaticamente al crear un objeto RepoJson
        self.ruta_archivo = ruta_archivo
        #Si no existe, se crea el archivo automaticamente 
        self.crear_db_si_no_existe()#Funcion

    #Metodo que crea una plantilla inicial en el archivo json
    def estructura_inicial(self):
        #Modificar segun su tema asignado
        return {
            "eventos": [],
            "asistentes": [],
            "entradas": [],
            "organizadores": [],
            "venues": [],
            "patrocinadores": []
        }

    #Metodo para crear el archivo .json en caso de que no exista
    def crear_db_si_no_existe(self):
        #Se obtiene el nombre de la carpeta almacenado en la ruta
        carpeta = os.path.dirname(self.ruta_archivo)#"data" (str)
        #Se valida que se obtenga un nombre
        if carpeta:
            #Se crea una carpeta con el nombre obtenido de la ruta
            #exist_ok=True. En caso que la carpeta ya exista, no la crea
            os.makedirs(carpeta, exist_ok=True)

        #Se pregunta si el archivo .json no existe
        if not os.path.exists(self.ruta_archivo):
            #Abrir/crear el archivo en modo de escritura
            with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
                #Se guarda el archivo con la estructura inicial en formato JSON
                #indent=4 le da un espaciado a los datos que se van a guardar en el archivo
                #ensure_ascii=False permite trabajar con caracteres especiales
                json.dump(self.estructura_inicial(), archivo, indent=4, ensure_ascii=False)

    #Metodo para leer el archivo json
    def leer_db(self):
        #Se crea el archivo en cado de que no exista
        self.crear_db_si_no_existe()
        #Se apertura el archivo en formato de lectura ("f")
        with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
            #Bloque de manejo de errores
            try:#Intentar ejecutar un codigo que podria faltar
                #Carga y conversion de datos JSON a un diccionario Python
                #Deserializacion
                return json.load(archivo)
            #Si el contenido del archivo esta corrupto, dañado, vacio
            except json.JSONDecodeError:
                #Retornar la estructura inicial por defecto
                return self.estructura_inicial()

    #Metodo para guardar(de forma fisica) en el archivo JSON
    def guardar_db(self, data):
        #Aperturar el archivo en modo escritura ("w")
        with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
            #Guardar o sobreescribir nuevos datos
            json.dump(data, archivo, indent=4, ensure_ascii=False)

    #Metodos para listar los registros de una coleccion
    #Coleccion hace referncia al listado con el que va a trabajar
    #solo_activos=True unicamente van a alistar aquellos registros activos
    def listar(self, coleccion, solo_activos=True):#coleccion: str = "personas"
        #Leer todo el archivo .json
        data = self.leer_db()
        #Se obtiene los registros que pertenecen a la coleccion establecia
        
        registros = data.get(coleccion, [])#Si no existe una coleccion en la variable registro se almacenara un listado vacio

        if solo_activos:
            return [registro for registro in registros if registro.get("estado") is True]
            #Se retorna una lista con registros que este en estado True
        return registros #Retornar todos los registros sin importar el estado

    #Metodo para guardar un nuevo registro
    def guardar(self, coleccion, registro):
        #Leer el archivo json
        data = self.leer_db()
        #Se pregunta si la coleccion o el listado no esta en data
        if coleccion not in data:
            data[coleccion] = [] #Se crea una nueva colecciona vacia con el nombre que buscamos si no existe
        data[coleccion].append(registro) #Los registro se guardan en memoria RAM
        self.guardar_db(data) #Guarda de forma fisica el nuevo registro

    #Metodo para buscar un registro mediante su ID
    #coleccion hace referencia al listado donde se realizara la busqueda
    #id_registro representa el ID que se desea buscar
    #solo_activos=True permite buscar unicamente registros activos
    def buscar_por_id(self, coleccion, id_registro, solo_activos=True):
        #Obtener todos los registros de la coleccion
        #solo_activos=False permite recorrer todos los registros sin importar su estado
        registros = self.listar(coleccion, solo_activos=False)
        
        #Recorrer cada registro de la coleccion
        for registro in registros:
            #Comparar el ID del registro con el ID enviado por el usuario
            if registro.get("id") == id_registro:
                
                #Validar si solo se desean registros activos
                if solo_activos and registro.get("estado") is not True:
                    #Retornar None si el registro esta inactivo
                    return None
                
                #Retornar el registro encontrado
                return registro

        #Retornar None si no existe coincidencia
        return None

    #Metodo para buscar un registro mediante cualquier campo
    #coleccion hace referencia al listado donde se realizara la busqueda
    #campo representa la clave que se desea comparar
    #valor representa el dato que se desea buscar
    #solo_activos=True permite buscar unicamente registros activos
    def buscar_por_campo(self, coleccion, campo, valor, solo_activos=True):
        #Obtener todos los registros de la coleccion
        #solo_activos=False permite recorrer todos los registros sin importar su estado
        registros = self.listar(coleccion, solo_activos=False)
        
        #Recorrer cada registro almacenado en la coleccion
        for registro in registros:
            #Comparar el valor del campo con el valor ingresado por el usuario
            #str() permite evitar errores de comparacion entre diferentes tipos de datos
            if str(registro.get(campo)) == str(valor):
                
                #Validar si solo se desean registros activos
                if solo_activos and registro.get("estado") is not True:
                    #Retornar None si el registro esta inactivo
                    return None
                #Retornar el registro encontrado
                return registro
        #Retornar None si no existe coincidencia
        return None

    #Metodo para actualizar registros
    def actualizar(self, coleccion, id_registro, nuevos_datos):
        #Leer datos del archivo
        data = self.leer_db()
        #Obtener los registros de una coleccion especifica
        registros = data.get(coleccion, [])

        for registro in registros:
            #Comparar el id del registro vs el id ddel registro que quiere modificar el usuario
            if registro.get("id") == id_registro:
                #Se actualiza los datos del registro con nuevos datos
                registro.update(nuevos_datos) #Memoria RAM (Local)
                self.guardar_db(data) #Se guarda los cambios en el archivo JSON
                return True #La actualizacion fue exitosa


        return False #No se encontraron registros

    #Metodo para eliminar de forma logica un registro
    def eliminar_logico(self, coleccion, id_registro):
        #Leer datos del archivo
        data = self.leer_db()
        #Obtener los registros de una coleccion especifica
        registros = data.get(coleccion, [])

        for registro in registros:
            #Comparar el id del registro vs el id ddel registro que quiere modificar el usuario
            if registro.get("id") == id_registro:
                #Se actualiza los datos del registro con nuevos datos
                registro["estado"] = False #Reasignacion que se hace en RAM
                self.guardar_db(data) #Se guarda los cambios en el archivo JSON
                return True #La eliminacion fue exitosa

        return False #No se encontraron registros
    
    
    