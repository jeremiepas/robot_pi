from gevent import monkey
monkey.patch_all()

import cgi
import redis
from flask import Flask, render_template, request
from flask_socketio import SocketIO
# import motors

app = Flask(__name__)
db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)

# motorL = motors.Motor(27,18,1)
# motorR = motors.Motor(22,17,0)
# car = motors.Motorcar(motorL, motorR)

@app.route('/')
def main():
    return render_template('main.html')


@app.route('/pymeetups/')
def pymeetups():
    return render_template('pymeetups.html')


@socketio.on('connect', namespace='/dd')
def ws_conn():
    socketio.emit('msg', namespace='/dd')


@socketio.on('disconnect', namespace='/dd')
def ws_disconn():
    socketio.emit('msg', namespace='/dd')
    # c = db.decr('connected')

@socketio.on('motor', namespace='/dd')
def ws_city(message):
    print(message)
    # car.forward(message['motorL'], message['motorR'])
    socketio.emit('motor', {'motor': cgi.escape(message['motor'])})

if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=5000)
