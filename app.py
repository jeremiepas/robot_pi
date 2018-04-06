import cgi
import redis
import cv2
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO
import threading
# import motors

app = Flask(__name__, static_url_path='/static')
db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)

cap = cv2.VideoCapture(0)

# motorR = motors.Motor(27,17,1)
# motorL = motors.Motor(22,18,1)
# car = motors.Motorcar(motorL, motorR)

@app.route('/')
def main():
    return render_template('index.html')



@app.route('/pymeetups/')
def pymeetups():
    return render_template('main.html')

def gen():
    """Video streaming generator function."""
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
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
        # car.forward(int(message['motorL']), int(message['motorR']))
    else:
        # car.rearward(int(message['motorL']), int(message['motorR']))
        pass
    # socketio.emit('motor', {'motor': cgi.escape(message['motor'])})

if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", debug=True, threaded=True)
