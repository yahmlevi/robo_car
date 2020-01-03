#!/usr/bin/env python

from steering_servo import SteeringServo

def test():
	import time
	servo = SteeringServo(debug=True)
	DELAY = 0.01
	try:
		angle = 90
		servo.write(angle)
		print("Turn to angle", angle)

		angle = 45
		servo.write(angle)
		print("Turn to angle", angle)

		angle = 135
		servo.write(angle)
		print("Turn to angle", angle)

		
	except KeyboardInterrupt:
		print("KeyboardInterrupt, steering stopped")
		# back_wheels.stop()

	finally:
		# print("Finished, motor stop")
		# back_wheels.stop()

		angle = 90
		servo.write(angle)
		print("Turn to angle", angle)

if __name__ == '__main__':
	test()

