# Conexion con web services

import requests # Peticiones al servidor 
import json # Trabajar con los archivos json

_ruta_base = 'http://intranet.itssacad.edu.ec/serviciosWebItss/public/api/v1/'
_obtenerDocente = _ruta_base + 'docente/obtenerDocente/{}' # Cedula del estudiante
_obtenerEstudiante = _ruta_base + 'estudiante/obtenerEstudiante/{}' # Cedula del estudiante
_obtenerEstudianteAcademico = _ruta_base + 'estudiante/obtenerEstudianteAcademico/{}' #Cedula del estudiante
_carreras = _ruta_base + 'general/carreras'
_secciones = _ruta_base + 'general/secciones'
_paralelos = _ruta_base + 'general/paralelos'
_listadoCiclosCarrera = _ruta_base + 'ciclos/listadoCiclosCarrera/{}' # Carrera
_listadoEstudiantesCarrera = _ruta_base + 'estudiante/listadoEstudiantesCarrera/{}' # Carrera
_listadoEstudiantesCarreraCiclo = _ruta_base + 'estudiante/listadoEstudiantesCarreraCiclo/{}/{}' # Carrera / ciclo
_listadoEstudiantesEspecificos = _ruta_base + 'estudiante/listadoEstudiantesEspecificos/{}/{}/{}' # Carrera / ciclo / seccion
_listadoDocentesPeriodoActual = _ruta_base + 'docente/listadoDocentesPeriodoActual'

# http://www.solveet.com/exercises/Cifrado-Cesar/145/solution-2126
def __user():
    user = 'dannyors18@gmail.com'
    key = 'GDQQ\\U3ef'
    password = ''
    for caracter in key:
        password = password + chr(ord(caracter) - 3)
    return (user, password)

def _connect_url(enlace, *args):
    if len(args) == 2:
        response = requests.get(enlace.format(args[0], args[1]), auth=__user()) 
    elif len(args) == 1:
        print enlace.format(args[0])
        response = requests.get(enlace.format(args[0]), auth=__user()) 
    else:
        response = requests.get(enlace, auth=__user())
    return response # retorna 200 si la coneccion es exitoso 

# Retorna un booleano True si se conecto con los datos de la web services
def conexion_web(enlace, *args):
    print 'ok'
    response = _connect_url(enlace, *args)
    if response.status_code == 200:
        connect = True
    else:
        connect = False
    return connect

# Retorna los datos de la web services en json
def get_data(enlace, *args):
    response = _connect_url(enlace, *args)
    if response.status_code == 200:
        vals = response.json()
    else: 
        vals = {}
    return vals.get('data')

# Retorna todos las clave q tiene un objeto 
def get_keys(data):
    result = []
    for value in data[0]:
        result.append(value)
    return tuple(result)

# Retorna todos los valores de los diccionarios de claves especificadas por parametro
def get_values(data, *args):
    result = []
    for i in range(len(data)):
        valor = {}
        for c in range(len(args)):
            valor.update({args[c]: data[i][args[c]]})
        result.append(valor)
    return tuple(result)

# Obtiene un objeto de una lista de objetos por busqueda perzonalizada de clave, valor
def get_object(data, dic): # data(diccionario de objetos), dic(diccionario de busqueda)
    # Cantidad de datos
    result = {}
    for i in range(len(data)):
        # iteramos el diccionario por cada lista
        for key, value in data[i].iteritems():
            # Evaluamos si la llave del diccionario dic coincide con con la llave
            # del diccionaro de la lista i
            if dic.keys()[0] == key:
                # Evaluamos si el valor del diccionario dic con llave del diccionario de la lista
                # coincide con el valor del diccionario de la lista i
                if dic[key] == value:
                    # Si todo concide reemplazamos la variable result con el valor de la variable q itero
                    result = data[i]
                    break
    return tuple(result)

# Obtiene varios objetos de otra lista de objetos por busqueda perzonalizada de clave, valor
def get_object_filter(data, dic):
    result = []
    for i in range(len(data)):
        for key, value in data[i].iteritems():
            if dic.keys()[0] == key:
                if dic[key] == value[:len(dic[key])]:
                    result.append(data[i])
    return tuple(result)

###
#   json.loads(objeto-json) # Cambia un json a diccionario
#   json.dumps(objeto-diccionario) # Cambia un diccionario a json