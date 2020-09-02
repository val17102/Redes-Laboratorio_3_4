import socketio
import dijkstra
import math
from copy import deepcopy


### Iniciar variables para almacenamiento de nodos conectados
nodosConectados = []

tablaConexionesPesos = []
nombreNodo = ''

### Variable global para flooting
sequenceNumber = 0

### Conectar al server
sio = socketio.Client()

### Definicion de las funciones de los 3 algoritmos
def flooding(data):
    global sequenceNumber, tablaConexionesPesos
    mensajeEnvio = {}

    ### Obtenemos las variables del mensaje
    emisorOriginal = data['emisor_original']
    emisor = data['emisor']
    receptor = data['receptor']
    receptorFinal = data['receptor_final']
    mensaje = data['mensaje']
    algoritmo = data['algoritmo']
    sequenceNo = data['sequence_no']
    pathAppender = data['path_appender']
    saltos = data['saltos']
    distancia = data['distancia']


    if sequenceNumber != 1:
        ### Actualizamos que ya recibimos este paquete
        sequenceNumber = 1

        ### El algoritmo revisa quienes son sus nodos vecinos
        misConexionesVecinas = []
        for arista in tablaConexionesPesos:
            if (arista[0] == nombreNodo) or (arista[1] == nombreNodo):
                misConexionesVecinas.append(arista)

        ### Se excluye al nodo fuente
        if emisor != nombreNodo:
            saltos = saltos + 1
            contadorVecinos = 0
            for arista in misConexionesVecinas:
                if (arista[0] == emisor) or (arista[1] == emisor):
                    misConexionesVecinas.pop(contadorVecinos)
                contadorVecinos = contadorVecinos + 1

        ### Se arma el mensaje hacia los vecinos restantes
        for arista in misConexionesVecinas:
            destino = ''
            if (arista[0] == nombreNodo):
                destino = arista[1]
            else:
                destino = arista[0]

            peso = distancia
            peso = peso + arista[2]

            subPathAppender = deepcopy(pathAppender)
            subPathAppender.append(nombreNodo)

            ### Se hacen logs de que el mensaje paso por aqui y su status
            #print('\n-----------------------------------------------------\n')
            #print('\nEl paso por aqui.\n')
            #print('\nNodo fuente: ' + str(emisor) + '\n')
            #print('\nNodo destino: ' + str(destino) + '\n')
            #print('\nSaltos recorridos: ' + str(saltos) + '\n')
            #print('\nDistancia: ' + str(peso) + '\n')
            #print('\nListado de nodos usados: ' + str(subPathAppender) + '\n')
            #print('\nMensaje: ' + str(mensaje) + '\n')
            #print('\n-----------------------------------------------------\n')

            mensajeEnvio = {
                'emisor_original': emisorOriginal,
                'emisor': nombreNodo,
                'receptor': destino,
                'receptor_final': receptorFinal,
                'mensaje': mensaje,
                'algoritmo': 'flooding',
                'sequence_no': 0,
                'path_appender': subPathAppender,
                'saltos': saltos,
                'distancia': peso
            }
    
            sio.emit(
                'my_response',
                mensajeEnvio
            )
        print("\nElije una opcion:\n1. Enviar contenido\n2. Agregar aristas\n3. Cambiar peso de arista\n4. Consultar tabla de pesos\n5. Salir\n>> ")
    else:
        print('\nEl parquete ya se recibió una vez anteriormente.\n')
        print("\nElije una opcion:\n1. Enviar contenido\n2. Agregar aristas\n3. Cambiar peso de arista\n4. Consultar tabla de pesos\n5. Salir\n>> ")

def linkStateRouting(data):
    grafoDatos = []
    mensajeEnvio = {}
    for conexion in tablaConexionesPesos:
        grafoDatos.append((conexion[0], conexion[1], conexion[2])) 
        grafoDatos.append((conexion[1], conexion[0], conexion[2]))
    
    graph = dijkstra.Graph(grafoDatos)
    data['receptor'] = graph.dijkstra(data["emisor"], data["receptor_final"])[1]
    for conexion in tablaConexionesPesos:
        if ((conexion[0] == data['emisor'] and conexion[1] == data['receptor']) or (conexion[1] == data['emisor'] and conexion[0] == data['receptor'])):
            data['distancia'] = data['distancia'] + conexion[2]
    data['path_appender'].append(nombreNodo)
    mensajeEnvio = data
    
    sio.emit(
        'my_response',
        mensajeEnvio
    )

def distanceVectorRouting(data):
    global tablaConexionesPesos, nodosConectados
    mensajeEnvio = {}

    ### Obtenemos las variables del mensaje
    emisorOriginal = data['emisor_original']
    emisor = data['emisor']
    receptor = data['receptor']
    receptorFinal = data['receptor_final']
    mensaje = data['mensaje']
    algoritmo = data['algoritmo']
    sequenceNo = data['sequence_no']
    pathAppender = data['path_appender']
    saltos = data['saltos']
    distancia = data['distancia']

    ### Se crea la tabla inicial con los vecinos y aristas que se conocen
    ### Estructura de la tabla [Destination, Distance, Next, Path]
    tablaNodo = []
    tablaNodoFinal = []
    for nodo in nodosConectados:
        if nodo != nombreNodo:
            for arista in tablaConexionesPesos:
                if (nombreNodo == arista[0]) and (nodo == arista[1]):
                    tablaNodo.append([arista[1],arista[2],arista[1],[nombreNodo,arista[1]], False])
                elif (nombreNodo == arista[1]) and (nodo == arista[0]):
                    tablaNodo.append([arista[0],arista[2],arista[0],[nombreNodo,arista[0]], False])

    ciclo = True
    ### Se realiza el proceso hasta que la tabla este completa
    while ciclo: 
        ### Verificar si la tabla ya esta completa
        contadorCompletos = 0
        for registro in tablaNodo:
            if registro[4] == True:
                contadorCompletos = contadorCompletos + 1

        if contadorCompletos == len(tablaNodo):
            ciclo = False

        else:
            nuevosRegistros = []
            tablaNodoCopia = deepcopy(tablaNodo)
            contadorVueltas = 0
            arregloPosiciones = []
            ### Procedimiento de creacion de relaciones
            for registro in tablaNodoCopia:
                if registro[4] == False:
                    for arista in tablaConexionesPesos:
                        conexiones = []
                        if (registro[0] == arista[0]) and (arista[1] not in registro[3]):
                            path = deepcopy(registro[3])
                            path.append(arista[1])
                            conexiones.append([arista[1],arista[2]+registro[1],registro[2],deepcopy(path), False])
                        elif (registro[0] == arista[1]) and (arista[0] not in registro[3]):
                            path = deepcopy(registro[3])
                            path.append(arista[0])
                            conexiones.append([arista[0],arista[2]+registro[1],registro[2],deepcopy(path), False])

                        nuevosRegistros = nuevosRegistros + conexiones
                    arregloPosiciones.append(contadorVueltas)
                else:
                    pass
                contadorVueltas = contadorVueltas + 1
                
            tablaNodo = tablaNodo + nuevosRegistros

            ### Actualizar el estado de cada nodo expandido
            for posicion in arregloPosiciones:
                tablaNodo[posicion][4] = True

    ### Reducir la tabla de nodos hasta tener los mas cortos a cada nodo
    tablaNodoReducida = []
    for nodo in nodosConectados:
        distanciaCorta = math.inf
        cantidadSaltos = math.inf
        caminoCorto = []
        if nodo != nombreNodo:
            for camino in tablaNodo:
                if (camino[0] == nodo) and (camino[1] <= distanciaCorta):
                    if (camino[1] == distanciaCorta) and (len(camino[3]) < cantidadSaltos):
                        caminoCorto = camino
                        distanciaCorta = camino[1]
                        cantidadSaltos = camino[3]
                    elif camino[1] < distanciaCorta:
                        caminoCorto = camino
                        distanciaCorta = camino[1]
                        cantidadSaltos = camino[3]
            tablaNodoReducida.append(caminoCorto)

    ### Obtener el nodo a interes para llegar al destino
    destino = ''
    for ruta in tablaNodoReducida:
        if ruta[0] == receptorFinal:
            destino = ruta[2]

    ### Buscar nuevamente en la tabla de conexiones el peso
    peso = 0
    for tab in tablaConexionesPesos:
        if ((nombreNodo == tab[0]) and (destino == tab[1])) or ((nombreNodo == tab[1]) and (destino == tab[0])):
            peso = tab[2]

    pathAppender.append(nombreNodo)

    ### Preparar el mensaje para enviar
    mensajeEnvio = {
        'emisor_original': emisorOriginal,
        'emisor': nombreNodo,
        'receptor': destino,
        'receptor_final': receptorFinal,
        'mensaje': mensaje,
        'algoritmo': 'dvr',
        'sequence_no': 0,
        'path_appender': pathAppender,
        'saltos': saltos + 1,
        'distancia': distancia + peso
    }

    sio.emit(
        'my_response',
        mensajeEnvio
    )

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    global tablaConexionesPesos, sequenceNumber
    algoritmo = data['algoritmo']
    nodoFinal = data['receptor_final']
    mensajeAEnviar = {}

    if nodoFinal != nombreNodo:
        ### Mandar a llamar al algoritmo correspondiente
        if algoritmo == 'flooding':
            print("\nFLOODING: Paso intermedio mensaje de ", data['emisor_original'], " hacia ", data['receptor_final'],"\n")
            flooding(data)
        elif algoritmo == 'dvr':
            print("\nDVR: Paso intermedio mensaje de ", data['emisor_original'], " hacia ", data['receptor_final'],"\n")
            print("\nElije una opcion:\n1. Enviar contenido\n2. Agregar aristas\n3. Cambiar peso de arista\n4. Consultar tabla de pesos\n5. Salir\n>> ")
            distanceVectorRouting(data)
        elif algoritmo == 'lsr':
            data['emisor'] = nombreNodo
            data['receptor'] = ''
            print("\nLSR: Paso intermedio mensaje de ", data['emisor_original'], " hacia ", data['receptor_final'],"\n")
            print("\nElije una opcion:\n1. Enviar contenido\n2. Agregar aristas\n3. Cambiar peso de arista\n4. Consultar tabla de pesos\n5. Salir\n>> ")
            data['saltos'] = data['saltos'] + 1
            linkStateRouting(data)
    else:
        if algoritmo == 'flooding':
            if sequenceNumber != 1:
                sequenceNumber = 1
                #print('Mensaje recibido: ' + str(data['mensaje']))
                emisorOriginal = data['emisor_original']
                emisor = data['emisor']
                receptor = data['receptor']
                receptorFinal = data['receptor_final']
                mensaje = data['mensaje']
                algoritmo = data['algoritmo']
                sequenceNo = data['sequence_no']
                pathAppender = data['path_appender']
                saltos = data['saltos']
                distancia = data['distancia']

                subPathAppender = deepcopy(pathAppender)
                subPathAppender.append(nombreNodo)

                ### Se hacen logs de que el mensaje paso por aqui y su status
                print('\n-----------------------------------------------------\n')
                print('\nEl mensaje llego a su destino.\n')
                print('\nNodo fuente: ' + str(emisorOriginal) + '\n')
                print('\nNodo destino: ' + str(receptorFinal) + '\n')
                print('\nSaltos recorridos: ' + str(saltos + 1) + '\n')
                print('\nDistancia: ' + str(distancia) + '\n')
                print('\nListado de nodos usados: ' + str(subPathAppender) + '\n')
                print('\nMensaje: ' + str(mensaje) + '\n')
                print('\n-----------------------------------------------------\n')

                print("\nElije una opcion:\n1. Enviar contenido\n2. Agregar aristas\n3. Cambiar peso de arista\n4. Consultar tabla de pesos\n5. Salir\n>> ")

                sio.emit(
                    'broadcast_reiniciar_sequence_number',
                    {
                        'nombre': nombreNodo
                    }
                )
        elif algoritmo == 'dvr':
            emisorOriginal = data['emisor_original']
            receptorFinal = data['receptor_final']
            mensaje = data['mensaje']
            algoritmo = data['algoritmo']
            distancia = data['distancia']
            pathAppender = data['path_appender']
            saltos = data['saltos']
            pathAppender.append(nombreNodo)

            print('\n-----------------------------------------------------\n')
            print('\nEl mensaje llego a su destino.\n')
            print('\nNodo fuente: ' + str(emisorOriginal) + '\n')
            print('\nNodo destino: ' + str(receptorFinal) + '\n')
            print('\nSaltos recorridos: ' + str(saltos) + '\n')
            print('\nListado de nodos usados: ' + str(pathAppender) + '\n')
            print('\nDistancia: ' + str(distancia) + '\n')
            print('\nMensaje: ' + str(mensaje) + '\n')
            print('\n-----------------------------------------------------\n')

            print("\nElije una opcion:\n1. Enviar contenido\n2. Agregar aristas\n3. Cambiar peso de arista\n4. Consultar tabla de pesos\n5. Salir\n>> ")

        elif algoritmo == 'lsr':
            emisorOriginal = data['emisor_original']
            receptorFinal = data['receptor_final']
            mensaje = data['mensaje']
            algoritmo = data['algoritmo']
            distancia = data['distancia']
            pathAppender = data['path_appender']
            saltos = data['saltos']
            pathAppender.append(nombreNodo)

            print('\n-----------------------------------------------------\n')
            print('\nEl mensaje llego a su destino.\n')
            print('\nNodo fuente: ' + str(emisorOriginal) + '\n')
            print('\nNodo destino: ' + str(receptorFinal) + '\n')
            print('\nSaltos recorridos: ' + str(saltos + 1) + '\n')
            print('\nListado de nodos usados: ' + str(pathAppender) + '\n')
            print('\nDistancia: ' + str(distancia) + '\n')
            print('\nMensaje: ' + str(mensaje) + '\n')
            print('\n-----------------------------------------------------\n')

            print("\nElije una opcion:\n1. Enviar contenido\n2. Agregar aristas\n3. Cambiar peso de arista\n4. Consultar tabla de pesos\n5. Salir\n>> ")

@sio.event
def disconnect():
    print('disconnected from server')

@sio.event
def recibir_conectados(data):
    global nodosConectados
    nodosConectados = data['nodos_conectados']

@sio.event
def recibir_tabla_conexiones(data):
    global tablaConexionesPesos
    tablaConexionesPesos = data['tabla_conexiones']

@sio.event
def reiniciar_sequence_number(data):
    global sequenceNumber
    sequenceNumber = 0

IP = input('Ingrese la IP a la que se conectara: ')
PORT = input('Ingrese el puerto al que se conectara: ')

sio.connect('http://'+str(IP)+':'+str(PORT))

### Inputs para configurar el nodo
nombreNodo = input('Ingresa el nombre del nodo: ')

### Mandarle al puente para agregar a la lista de conectados
sio.emit(
    'conectado_por_nombre',
    {
        'nombre': nombreNodo
    }
)

sio.emit(
    'solicitar_tabla_conectados',
    {
        'nombre': nombreNodo
    }
)

sio.emit(
    'solicitar_tabla_aristas',
    {
        'nombre': nombreNodo
    }
)

### Esperar al server
while not nodosConectados:
    pass

### Quitamos el nodo propio
nodosConectados.remove(nombreNodo)
print('\nNodos conectados a la red: ' + str(nodosConectados))

### Realizamos las conexiones que el usuario quiera
opcion = ''
ciclo = True
while ciclo and nodosConectados:
    opcion = int(input("\nDesea ingresar una conexion entre nodos\n1. Si\n2. No\n>> "))
    if opcion == 1:
        ### Crear la conexion mandandole la info
        while nombreNodo in nodosConectados:
            nodosConectados.remove(nombreNodo)
        print(nodosConectados)
        opcionesNodos = ''
        contador = 0
        for i in nodosConectados:
            opcionesNodos = opcionesNodos + '\n' + str(contador) + '. ' + str(i)
            contador = contador + 1
        opcionesNodos = opcionesNodos + '\n>> '
        posicionNodoAConectar = int(input('Ingrese el numero de opcion correspondiente al nodo al cual desea conectarse:' + opcionesNodos))
        if posicionNodoAConectar >= 0 and posicionNodoAConectar <= len(nodosConectados) - 1:
            conexionYaRealizada = False
            for nodo in tablaConexionesPesos:
                if (nodo[0] == nodosConectados[posicionNodoAConectar] and nodo[1] == nombreNodo) or (nodo[0] == nombreNodo and nodo[1] == nodosConectados[posicionNodoAConectar]) :
                    conexionYaRealizada = True
                    break
            if not conexionYaRealizada:
                nodoAConectar = nodosConectados[posicionNodoAConectar]
                pesoNodoAConectar = int(input('Ingrese el peso de la arista para la conexion entre ' + str(nombreNodo) + ' y ' + str(nodoAConectar) + '\n>> '))
                tablaConexionesPesos.append([nombreNodo, nodoAConectar, pesoNodoAConectar])
                sio.emit(
                    'broadcast_tabla',
                    {
                        'tabla_conexiones' : tablaConexionesPesos
                    }
                )
            else:
                print('\nLa conexion ha sido realizada entre estos nodos')    
        else:
            print('\nOpcion invalida')
    else:
        ciclo = False
        print('\nNodo ha terminado de configurarse')

### Se notifica que el nodo fue configurado correctamente
print('\nNodo conectado a la red')

while True:
    print("\nElije una opcion:\n1. Enviar contenido\n2. Agregar aristas\n3. Cambiar peso de arista\n4. Consultar tabla de pesos\n5. Salir")
    opcion = int(input('>> '))
    if opcion == 1:
        mensaje = 'HELLO WORLD'

        ### Se manda a llamar al algoritmo correspondiente aqui
        algoritmo = int(input("\nSeleccione el algorimo a utilizar\n1. Flooding\n2. Distance vector routing\n3. Link state routing\n>> "))
        while nombreNodo in nodosConectados:
            nodosConectados.remove(nombreNodo)
        print(nodosConectados)
        opcionesNodos = ''
        contador = 0
        for i in nodosConectados:
            opcionesNodos = opcionesNodos + '\n' + str(contador) + '. ' + str(i)
            contador = contador + 1
        opcionesNodos = opcionesNodos + '\n>> '
        opcionEleccionNodo = int(input('Ingrese el numero de opcion correspondiente al nodo al cual desea conectarse:' + opcionesNodos))
        if opcionEleccionNodo >= 0 and opcionEleccionNodo <= len(nodosConectados) - 1:
            eleccionNodo = nodosConectados[opcionEleccionNodo]
            print(eleccionNodo)
            mensaje = input("\nIngrese el mensaje que desea enviar\n>> ")

            ### Envio del mensaje
            if algoritmo == 1:
                ### Algoritmo Flooding
                ### Construccion mensaje
                mensajeAEnviar = {
                        'emisor_original': nombreNodo,
                        'emisor': nombreNodo, 
                        'receptor': nombreNodo,
                        'receptor_final': eleccionNodo,
                        'mensaje': mensaje,
                        'algoritmo': 'flooding',
                        'sequence_no': 0,
                        'path_appender': [],
                        'saltos': 0,
                        'distancia': 0
                    }
                flooding(mensajeAEnviar)
            elif algoritmo == 2:
                ### Algoritmo DVR
                mensajeAEnviar = {
                        'emisor_original': nombreNodo,
                        'emisor': nombreNodo, 
                        'receptor': '',
                        'receptor_final': eleccionNodo,
                        'mensaje': mensaje,
                        'algoritmo': 'dvr',
                        'sequence_no': 0,
                        'path_appender': [],
                        'saltos': 0,
                        'distancia': 0
                    }
            
                distanceVectorRouting(mensajeAEnviar)
            elif algoritmo == 3:
                ### Algoritmo LSR
                mensajeAEnviar = {
                        'emisor_original': nombreNodo,
                        'emisor': nombreNodo, 
                        'receptor': '',
                        'receptor_final': eleccionNodo,
                        'mensaje': mensaje,
                        'algoritmo': 'lsr',
                        'sequence_no': 0,
                        'path_appender': [],
                        'saltos': 0,
                        'distancia': 0
                    }
            
                linkStateRouting(mensajeAEnviar)
            else:
                print('\nOpcion invalida')
        else:
            print('\nOpcion invalida')

    elif opcion == 2:
        ### Crear la conexion mandandole la info
        while nombreNodo in nodosConectados:
            nodosConectados.remove(nombreNodo)
        print(nodosConectados)
        if nodosConectados:
            opcionesNodos = ''
            contador = 0
            for i in nodosConectados:
                opcionesNodos = opcionesNodos + '\n' + str(contador) + '. ' + str(i)
                contador = contador + 1
            opcionesNodos = opcionesNodos + '\n>> '
            posicionNodoAConectar = int(input('Ingrese el numero de opcion correspondiente al nodo al cual desea conectarse:' + opcionesNodos))
            if posicionNodoAConectar >= 0 and posicionNodoAConectar <= len(nodosConectados) - 1:
                conexionYaRealizada = False
                for nodo in tablaConexionesPesos:
                    if (nodo[0] == nodosConectados[posicionNodoAConectar] and nodo[1] == nombreNodo) or (nodo[0] == nombreNodo and nodo[1] == nodosConectados[posicionNodoAConectar]) :
                        conexionYaRealizada = True
                        break
                if not conexionYaRealizada:
                    nodoAConectar = nodosConectados[posicionNodoAConectar]
                    pesoNodoAConectar = int(input('Ingrese el peso de la arista para la conexion entre ' + str(nombreNodo) + ' y ' + str(nodoAConectar) + '\n>> '))
                    tablaConexionesPesos.append([nombreNodo, nodoAConectar, pesoNodoAConectar])
                    sio.emit(
                        'broadcast_tabla',
                        {
                            'tabla_conexiones' : tablaConexionesPesos
                        }
                    )
                else:
                    print('\nLa conexion ha sido realizada entre estos nodos')    
            else:
                print('\nOpcion invalida')
        else:
            print('\nNo hay nodos para conectar')

    elif opcion == 3:
        misConexionesVecinas = []
        contadorVecino = 0
        for posibleVecino in tablaConexionesPesos:
            if (nombreNodo == posibleVecino[0]) or (nombreNodo == posibleVecino[1]):
                misConexionesVecinas.append([contadorVecino, posibleVecino])
            contadorVecino = contadorVecino + 1
        if misConexionesVecinas:
            contadorOpciones = 0
            opcionesNodosVecinos = ''
            for i in misConexionesVecinas:
                opcionesNodosVecinos = opcionesNodosVecinos + '\n' + str(contadorOpciones) + '. ' + str(i[1][0]) + ' <=> ' + str(i[1][1])
                contadorOpciones = contadorOpciones + 1
            opcionesNodosVecinos = opcionesNodosVecinos + '\n>> '
            posicionAristaModificar = int(input('Ingrese el numero de opcion correspondiente a la arista que desea modificar el peso:' + opcionesNodosVecinos))
            if posicionAristaModificar >= 0 and posicionAristaModificar <= len(misConexionesVecinas) - 1:
                ### Eliminamos la conexion actual
                vecinoSeleccionado = misConexionesVecinas[posicionAristaModificar]
                tablaConexionesPesos.pop(vecinoSeleccionado[0])
                ### Creamos una nueva conexion basada en los datos guardados
                aristaModificar = vecinoSeleccionado[1]
                pesoNuevo = int(input('Ingrese el peso nuevo de la arista: '))
                aristaModificar[2] = pesoNuevo
                ### Apendeamos la conexion con el peso nuevo
                tablaConexionesPesos.append(aristaModificar)
                ### Mandamos la tabla actualizada a todos
                sio.emit(
                    'broadcast_tabla',
                    {
                        'tabla_conexiones' : tablaConexionesPesos
                    }
                )
            else:
                print('\nOpcion invalida')
        else:
            print('\nNo hay aristas para modificar')
    elif opcion == 4:
        print('\nLa tabla de pesos es: \n')
        print(tablaConexionesPesos)
    elif opcion == 5:
        sio.disconnect()
        break

    else:
        print("Elija una opción válida")

print("Chao, Unistall")
