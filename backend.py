from cmath import log
from operator import imod
import socketio
import eventlet
from sql import SqlHelper
from mysql.connector import MySQLConnection


# create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*', always_connect=True)
# wrap with a WSGI application
app = socketio.WSGIApp(sio)
# the sql connector
sqlConn = None


@sio.event
def connect(sid, environ, auth):
    print("Successfully connected", sid)

# send message to the user in the same room(channel)
@sio.event
def smessage(sid, data):
    sio.emit(event='rmessage', data={"msg":data["content"], 
    "userId":data["userId"], "sex":data["sex"], "userName":data["userName"],
    "imgData":data["imgData"]}, room=data["groupId"], skip_sid=sid)
    print(sid + " successfully send message to the room " + data["groupId"]+", " + data["content"])

# login verification
@sio.event
def login(sid, data):
    mycursor = sqlConn.cursor()
    mycursor.execute("Select userId, sex, age from share_user where userName= %s and password= %s",(data["userName"],data["password"]))
    user = mycursor.fetchone()
    if user is not None:
        r = {"result":"success", "userId":user[0], "sex":user[1], "age":user[2]}
    else:
        r = {"result":"failed"}
    print("Successful login")
    sqlConn.commit()
    mycursor.close()
    return r

# register event
@sio.event
def register(sid, data):
    mycursor = sqlConn.cursor()
    mycursor.execute("INSERT INTO share_user (userName, `password`, sex, age) VALUES(%s, %s, %s, %s)", 
                        (data["userName"], data["password"], data["sex"], data["age"]))
    userId = mycursor.lastrowid
    if userId > 0:
        r = {"result":"success", "userId":userId}
    else:
        r = {"result":"failed"}
    sqlConn.commit()
    mycursor.close()
    return r

@sio.event
def updateUser(sid, data):
    mycursor = sqlConn.cursor()
    mycursor.execute("UPDATE share_user SET password=%s, sex=%s, age=%s where userId=%s",
                (data["password"], data["sex"], data["age"], data["userId"]))
    rowcount = mycursor.rowcount
    if rowcount > 0:
        r = {"result":"success"}
    else:
        r = {"result":"failed"}
    sqlConn.commit()
    mycursor.close()
    return r

# put user session into the room
@sio.event
def joinRoom(sid, data):
    sio.enter_room(sid, data["groupId"])
    # print("join the room "+ data["groupId"] + ", " + sid + "," + data["userId"])

# put user session into the room
@sio.event
def quitRoom(sid, data):
    sio.leave_room(sid, data["groupId"])
    # print("leave the room "+ data["groupId"] + ", " + sid + "," + data["userId"])

# disconnect from server
@sio.event
def disconnect(sid):
    rooms = sio.rooms(sid)
    for room in rooms:
        sio.leave_room(sid, room)
        print(sid + " leave room: " + room)
    print('disconnect ', sid)
    

if __name__ == '__main__':
    try:
        # create a mysql db connection
        sqlConn = SqlHelper.initDbInstance(SqlHelper)
        assert isinstance(sqlConn, MySQLConnection)
        # start server
        eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app, log_output=None)
    except SystemExit:
        print("Close the sql connector after eventlet server stop")
        sqlConn.close()
