import deepl
import socketio
import eventlet

# create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')

# wrap with a WSGI application
app = socketio.WSGIApp(sio)

def translate(source_text):
        return deepl.translate(source_language="EN", target_language="ZH", text=source_text)

@sio.event
def getChinese(sid, data):
    sio.emit("rtranslation", {"text":translate(data["text"]), "index":data["index"]})


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 7000)), app, log_output=None)