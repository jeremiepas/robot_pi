import RPi.GPIO as GPIO
import time

class Motor:

	def __init__(self, gpsens, gpspeed, sensdfault):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(gpspeed, GPIO.OUT)
		self.gpspeed = GPIO.PWM(gpspeed, 100)
		self.gpspeed.start(5)
		self.sensdfault = sensdfault
		GPIO.setup(gpsens, GPIO.OUT)
		self.gpsens =  gpsens

	def forward(self, speed):
		vi = float(speed) + 5
		GPIO.output(self.gpsens, self.sensdfault)
		self.gpspeed.ChangeDutyCycle(vi)


	def rearward(self, speed):
		vi = float(speed) + 5
		print(1 if self.sensdfault == 1 else 0)
		GPIO.output(self.gpsens,   1 if self.sensdfault == 1 else 0)
		self.gpspeed.ChangeDutyCycle(vi)

class Motorcar:

	def __init__(self, left, right):
	 	self.left = left
		self.right = right

	def forward(self, speedl, speedr):
		self.left.forward(speedl)
		self.right.forward(speedr)

	def rearward(self, speedl, speedr):
			self.left.rearward(speedl)
			self.right.rearward(speedr)
