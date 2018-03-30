import cgi
import redis
import cv2
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO
import threading
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

def gen():
    """Video streaming generator function."""
    template = cv2.imread('moi.jpg',0)
    w, h = template.shape[::-1]

    meth = 'cv2.TM_CCOEFF_NORMED'
    method = eval(meth)

    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Our operations on the frame come here
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # Display the resulting frame
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        cv2.imwrite('t.jpg', img)
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
        car.forward(int(message['motorL']), int(message['motorR']))
    else:
        car.rearward(int(message['motorL']), int(message['motorR']))

    # socketio.emit('motor', {'motor': cgi.escape(message['motor'])})

if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", threaded=True)
