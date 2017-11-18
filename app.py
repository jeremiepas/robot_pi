from gevent import monkey
monkey.patch_all()

import cgi
import redis
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from camera import VideoCamera
import motors
app = Flask(__name__, static_url_path='/static')
db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)

motorR = motors.Motor(27,17,1)
motorL = motors.Motor(22,18,1)
car = motors.Motorcar(motorL, motorR)

@app.route('/')
def main():
    return render_template('pymeetups.html')



@app.route('/pymeetups/')
def pymeetups():
    return render_template('main.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect', namespace='/dd')
def ws_conn():
    socketio.emit('msg', namespace='/dd')


@socketio.on('disconnect', namespace='/dd')
def ws_disconn():
    socketio.emit('msg', namespace='/dd')
    # c = db.decr('connected')

@socketio.on('motor', namespace='/dd')
def ws_city(message):
    if message['direction']:
        print(message['direction'])
        print(message['motorL'])
        car.forward(int(message['motorL']), int(message['motorR']))
    else:
        car.rearward(int(message['motorL']), int(message['motorR']))

    # socketio.emit('motor', {'motor': cgi.escape(message['motor'])})

if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=5000)
