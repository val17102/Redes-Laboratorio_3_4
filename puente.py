import eventlet
import socketio

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
def my_message(sid, data):
    ### TODO logica para mandar el mensaje al nodo correspondiente

    print('Mensaje recibido: ', data)

@sio.event
def disconnect(sid):
    ### Hay que manejar la desconexion de un nodo
    ### TODO obtener la referencia del nombre del nodo en nodosConectadosBySid
    ### TODO eliminar referencia de nodosConectadosBySid  
    ### TODO actualizar la tabla de todos haciendo un broadcast para eliminar el nodo por nombre
    ### TODO no olvidar actualizar la tabla de los demas y los nodos conectados 
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

PORT = int(input('Ingrese el puerto que utilizara: '))

eventlet.wsgi.server(eventlet.listen(('localhost', PORT)), app)