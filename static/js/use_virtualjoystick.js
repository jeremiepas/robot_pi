var url = "http://" + document.domain + ":" + location.port;
var socket = io.connect(url + "/dd");
console.log("touchscreen is", VirtualJoystick.touchScreenAvailable() ? "available" : "not available");

var joystick	= new VirtualJoystick({
container	: document.getElementById('img_jos'),
mouseSupport	: true,
});
joystick.addEventListener('touchStart', function(){
console.log('down')
})
joystick.addEventListener('touchEnd', function(){
console.log('up')
})
setInterval(function(){
  if (  joystick.right()) {
    socket.emit('motor', {'direction': 1, 'motorR': 0, 'motorL': 90})
  } else if (joystick.up()) {
    socket.emit('motor', {'direction': 1, 'motorR': 90, 'motorL': 90})
  }else if (  joystick.left()) {
    socket.emit('motor', {'direction': 1, 'motorR': 90, 'motorL': 0})
  }else if (joystick.down()) {
    socket.emit('motor', {'direction': 0, 'motorR': 90, 'motorL': 90})
  }else {
    socket.emit('motor', {'direction': 1, 'motorR': 0, 'motorL': 0})
  }

  var outputEl	= document.getElementById('result');
  outputEl.innerHTML	= '<b>Result:</b> '
    + ' dx:'+joystick.deltaX()
    + ' dy:'+joystick.deltaY()
    + (joystick.right()	? ' right'	: '')
    + (joystick.up()	? ' up'		: '')
    + (joystick.left()	? ' left'	: '')
    + (joystick.down()	? ' down' 	: '');
}, 1/30 * 10000);
