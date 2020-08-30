import eventlet
import socketio
import time

###I Iniciar variables para almacenamiento de nodos conectados
nodosConectadosBySid = []
tablaConexionesPesos = []

### Conectar el server
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_response(sid, data):
    ### Logica para mandar el mensaje al nodo correspondiente
    ### Se revisa a quien se mandara el mensaje
    receptor = data['receptor']

    ### Se busca el sid del receptor
    sidReceptor = ''
    for i in nodosConectadosBySid:
        if i[0] == receptor:
            sidReceptor = i[1]
            break

    ### Se envia por broadcast al receptor
    sio.emit(
        'my_message',
        data,
        room=sidReceptor
    )    

@sio.event
def disconnect(sid):
    global nodosConectadosBySid, tablaConexionesPesos
    ### Hay que manejar la desconexion de un nodo
    ### Obtener la referencia del nombre del nodo en nodosConectadosBySid
    nodo = ''
    contador = 0
    for i in nodosConectadosBySid:
        if i[1] == sid:
            nodo = i[0]
            break
        contador = contador + 1     

    ### Eiminar referencia de nodosConectadosBySid
    nodosConectadosBySid.pop(contador)

    ### Actualizar la tablaConexionesPesos
    contadorTabla = 0
    for j in tablaConexionesPesos:
        if (nodo == j[0]) or (nodo == j[1]):
            tablaConexionesPesos.pop(contadorTabla)
        contadorTabla = contadorTabla + 1

    ### Actualizar la tabla y nodos conectados a los demas
    nodosConectados = []
    for conexion in nodosConectadosBySid:
        nodosConectados.append(conexion[0])

    sio.emit(
        'recibir_conectados',
        {
            'nodos_conectados': nodosConectados
        }
    )

    sio.emit(
        'recibir_tabla_conexiones',
        {
            'tabla_conexiones': tablaConexionesPesos
        }
    )

    ### Imprimir desconexion
    print('disconnect ', sid)

@sio.event
def conectado_por_nombre(sid, data):
    global nodosConectadosBySid
    nodosConectadosBySid.append([data['nombre'], sid])  

@sio.event
def solicitar_tabla_conectados(sid, data):
    global nodosConectadosBySid
    nodosConectados = []
    for conexion in nodosConectadosBySid:
        nodosConectados.append(conexion[0])

    sio.emit(
        'recibir_conectados',
        {
            'nodos_conectados': nodosConectados
        }
    )

@sio.event
def solicitar_tabla_aristas(sid, data):
    global tablaConexionesPesos
    sio.emit(
        'recibir_tabla_conexiones',
        {
            'tabla_conexiones': tablaConexionesPesos
        }
    )

@sio.event
def broadcast_tabla(sid, data):
    ### Se hace un broadcast para actualizar todas las tablas
    global tablaConexionesPesos
    tablaConexionesPesos = data['tabla_conexiones']
    sio.emit(
        'recibir_tabla_conexiones',
        {
            'tabla_conexiones': data['tabla_conexiones']
        }        
    )

@sio.event
def broadcast_reiniciar_sequence_number(sid, data):
    print('Esperar un poco antes de reiniciar el sequence number')
    time.sleep(5)
    print('Sequence number de todos reiniciado')
    sio.emit(
        'reiniciar_sequence_number',
        {
            'nombre': 0
        }        
    )

PORT = int(input('Ingrese el puerto que utilizara: '))

eventlet.wsgi.server(eventlet.listen(('localhost', PORT)), app)