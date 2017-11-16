import motors

motorR = motors.Motor(27,17,1)
motorL = motors.Motor(22,18,1)
car = motors.Motorcar(motorL, motorR)

car.forward(95, 5)
car.forward(5,5)
