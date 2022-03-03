import socketio
import eventlet


# standard Python
sio = socketio.Client()


# UI里面请求随机电影微服务
#{
sio.connect('http://127.0.0.1:6000')
sio.emit("getRandomMovie",{})
#}


# service将随机电影名返回回来
@sio.event
def setRandomMovie(data):
    print(data)
    sio.disconnect()