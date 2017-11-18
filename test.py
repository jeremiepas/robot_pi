import motors
import time

motorR = motors.Motor(27,17,1)
motorL = motors.Motor(22,18,1)
car = motors.Motorcar(motorL, motorR)

car.forward(0, 90)
time.sleep(0.5)
car.forward(5,5)
