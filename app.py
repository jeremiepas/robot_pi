import cgi
import cv2
import asyncio
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO
import threading
import motors
import time

app = Flask(__name__, static_url_path='/static')
# db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)

cap = cv2.VideoCapture(0)

motorR = motors.Motor(27,17,1)
motorL = motors.Motor(22,18,1)
car = motors.Motorcar(motorL, motorR)


async def gen():
    """Video streaming generator function."""
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb+').read() + b'\r\n')
        time.sleep( 5 )
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def home():
    return render_template('index.html')

#
# acu = threading.Thread(target=test)
# acu.start()


@socketio.on('connect', namespace='/dd')
def ws_conn():
    socketio.emit('msg', namespace='/dd')


@socketio.on('disconnect', namespace='/dd')
def ws_disconn():
    socketio.emit('msg', namespace='/dd')
    # c = db.decr('connected')

@socketio.on('motor', namespace='/dd')
def ws_city(message):
    if message['direction'] == 1:
        car.forward(int(message['motorL']), int(message['motorR']))
    else:
        car.rearward(int(message['motorL']), int(message['motorR']))
        pass
    # socketio.emit('motor', {'motor': cgi.escape(message['motor'])})

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # backProc = Process(target=gen, args=())
    # backProc.start()
    socketio.run(app, "0.0.0.0",  debug=True, threaded=True)
