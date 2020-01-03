#!/usr/bin/env python

def test():
	import time
	back_wheels = Back_Wheels()
	DELAY = 0.01
	try:
		back_wheels.forward()
		for i in range(0, 100):
			back_wheels.speed = i
			print("Forward, speed =", i)
			time.sleep(DELAY)
		for i in range(100, 0, -1):
			back_wheels.speed = i
			print("Forward, speed =", i)
			time.sleep(DELAY)

		back_wheels.backward()
		for i in range(0, 100):
			back_wheels.speed = i
			print("Backward, speed =", i)
			time.sleep(DELAY)
		for i in range(100, 0, -1):
			back_wheels.speed = i
			print("Backward, speed =", i)
			time.sleep(DELAY)
	except KeyboardInterrupt:
		print("KeyboardInterrupt, motor stop")
		back_wheels.stop()
	finally:
		print("Finished, motor stop")
		back_wheels.stop()

if __name__ == '__main__':
	test()


        


