from cmath import log
import socketio
import eventlet

# create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*', always_connect=True)

# wrap with a WSGI application
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ, auth):
    print("Successfully connected", sid)

@sio.event
def smessage(sid, data):
    sio.emit(event='rmessage', data={"msg":data["content"], "userId":data["userId"]}, room=data["groupId"], skip_sid=sid)
    print(sid + " successfully send message to the room " + data["groupId"]+", " + data["content"])

@sio.event
def login(sid, data):
    r = {"result":"success", "userId":"123"}
    sio.emit('rlogin',r)
    print("Successful login")

@sio.event
def register(sid, data):
    sio.emit('rregister',"success")
    print("Successful login")

@sio.event
def joinRoom(sid, data):
    sio.enter_room(sid, data["groupId"])
    print("join the room "+ data["groupId"] + ", " + sid + "," + data["userId"])

@sio.event
def quitRoom(sid, data):
    sio.leave_room(sid, data["groupId"])
    print("leave the room "+ data["groupId"] + ", " + sid + "," + data["userId"])

@sio.event
def disconnect(sid):
    rooms = sio.rooms(sid)
    for room in rooms:
        sio.leave_room(sid, room)
        print(sid + " leave room: " + room)
    print('disconnect ', sid)
    

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app, log_output=None)