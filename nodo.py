import socketio

### Iniciar variables para almacenamiento de nodos conectados
nodosConectados = []

tablaConexionesPesos = []
nombreNodo = ''

### Conectar al server
sio = socketio.Client()

### TODO Definicion de las funciones de los 3 algoritmos

### EXAMPLE
### def flooding(param, param, etc):
###     codigo

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    ### TODO recibir la data y meterla en variables
    ### TODO mandar a llamar al algoritmo correspondiente

    ### TODO volver a mandar el mensaje con sio.emit de my_message si no es el nodo final

    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

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

        ### TODO Mandar a llamar al algoritmo correspondiente aqui
        ## algoritmo = int(input("\nSeleccione el algorimo a utilizar\n1. Flooding\n2. Distance vector routing\n3. Link state routing"))
        ## if algotimo == 1:
        ##      Algoritmo Chino 
        ##      ### Mandar a llamar a la funcion del algoritmo aqui

        ##      ### Construccion y emision del mensaje
        ##      sio.emit(
        ##          'my_message',
        ##          {
        ##              'emisor_original': mensaje
        ##          }
        ##      )

        ## elif algoritmo == 2:
        ##      Algoritmo Esturban
        ##      ### Mandar a llamar a la funcion del algoritmo aqui

        ##      ### Construccion y emision del mensaje
        ##      sio.emit(
        ##          'my_message',
        ##          {
        ##              'emisor_original': mensaje
        ##          }
        ##      )

        ## elif algoritmo == 3:
        ##      Algoritmo Miguel

        ##      ### Mandar a llamar a la funcion del algoritmo aqui

        ##      ### Construccion y emision del mensaje
        ##      sio.emit(
        ##          'my_message',
        ##          {
        ##              'emisor_original': mensaje
        ##          }
        ##      )

        ## else:
        ##      print('\nOpcion invalida')

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
