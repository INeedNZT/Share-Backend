import random
import socketio
import eventlet


# create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*', logger=False, engineio_logger=False)

# wrap with a WSGI application
app = socketio.WSGIApp(sio)

result_movie={
        "moviename":"007:无暇赴死",
        "movietype":"动作",
        "movieyear":2021,
        "wekiname":"No_Time_to_Die"
}
movie_type=""
movie_year=0
movie_language=""
setrandome=True
choose_movie=[
    {
        "moviename":"007:无暇赴死",
        "movietype":"动作",
        "movieyear":2021,
        "wekiname":"No_Time_to_Die",
        "movielanguage":"english"
    },
    {
        "moviename":"阿甘正传",
        "movietype":"喜剧",
        "movieyear":1994,
        "wekiname":"Forrest_Gump",
        "movielanguage":"english"
    },{
        "moviename":"赌神",
        "movietype":"喜剧",
        "movieyear":1989,
        "wekiname":"",
        "movielanguage":"普通话"
    },

]


def setflag(flag):
    global setrandome
    setrandome=flag


def set_param(movietype,movieyear,movielanguage):
    global movie_type,movie_year,movie_language
    movie_type=movietype
    if(movieyear!=""):
        movie_year=movieyear
    movie_language=movielanguage


def get_weki_url():
    return "en.wikipedia.org/wiki/"+result_movie["wekiname"]


def get_randommovie():
    global result_movie
    number = random.randint(0,len(choose_movie)-1)
    result_movie=choose_movie[number]
    return result_movie

def get_prefer():
    global result_movie
    temp_list=[]
    print(movie_year)
    print(movie_type)
    for item in choose_movie:
        if(item["movietype"]!=movie_type and item["movieyear"]>int(movie_year) and item["movielanguage"]!=movie_language):
            temp_list.append(item)
    number = random.randint(0, len(temp_list) - 1)
    result_movie = temp_list[number]
    return result_movie

@sio.event
def getRandomMovie(sid, data):
    sio.emit("setRandomMovie", get_randommovie())

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 6000)), app)