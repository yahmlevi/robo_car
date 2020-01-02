#!/usr/bin/env python

from front_wheels import Front_Wheels

def test(chn=0):
	import time
	front_wheels = Front_Wheels(channel=chn)
	try:
		while True:
			print("turn_left")
			front_wheels.turn_left()
			time.sleep(1)
			print("turn_straight")
			front_wheels.turn_straight()
			time.sleep(1)
			print("turn_right")
			front_wheels.turn_right()
			time.sleep(1)
			print("turn_straight")
			front_wheels.turn_straight()
			time.sleep(1)
	except KeyboardInterrupt:
		front_wheels.turn_straight()

if __name__ == '__main__':
	test()
