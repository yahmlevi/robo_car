#!/usr/bin/env python
'''
**********************************************************************
* Filename    : back_wheels.py
* Description : A module to control the back wheels of RPi Car
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-13    New release
*               Cavon    2016-11-04    fix for submodules
**********************************************************************
'''
import time
from file_db import FileDb
from front_wheel_drive_motor import Motor
from freenove.m_dev import mDev


device = mDev()

class FrontWheelDrive (object):

	''' Back wheels control class '''
	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "front_wheel_drive.py":'

	def __init__(self, debug=False, db="config"):
		''' Init the direction channel and pwm channel '''
		
		self.db = FileDb(db=db)

		# self.forward = int(self.db.get('forward', default_value=1))

		self.mdev = device

		self.left_wheel = Motor(motor="LEFT", device=self.mdev)
		self.right_wheel = Motor(motor="RIGHT", device=self.mdev)

		self._speed = 0
		self.current_speed = 0

		self.debug = debug
		# self._debug_('Set left wheel to #%d, PWM channel to %d' % (self.Motor_A, self.PWM_A))
		# self._debug_('Set right wheel to #%d, PWM channel to %d' % (self.Motor_B, self.PWM_B))

	def _debug_(self,message):
		if self._DEBUG:
			print(self._DEBUG_INFO,message)

	def forward(self):
		''' Move both wheels forward '''
		self.left_wheel.forward()
		self.right_wheel.forward()
		self._debug_('Running forward')

	def backward(self):
		''' Move both wheels backward '''
		self.left_wheel.backward()
		self.right_wheel.backward()
		self._debug_('Running backward')

	def stop(self):
		''' Stop both wheels '''
		self.speed(0)
		self._debug_('Stop')

	@property
	def speed(self, speed):
		return self._speed

	@speed.setter
	def speed(self, speed):
		self._debug_('Set speed to %s' % self._speed)
		self._speed = speed
		
		''' Set moving speeds '''
		min_speed = 500
		max_speed = 1000

		if speed != 0 and speed < min_speed: 
			speed = min_speed

		if speed > max_speed:
			speed = max_speed

		speed_change = 10
		sleep_time = 0.005

		# TODO: accelerate & decelerate
		self._debug_('Current speed is %s' % self.current_speed)
		if speed > self.current_speed: 
			speed_change = 10
		else:
			speed_change = -10

		self._debug_('Set speed change to %s' % speed_change)

		for value in range(self.current_speed, speed, speed_change):	
			self._debug_('Changing speed to %s' % value)

			self.left_wheel.speed = value
			self.right_wheel.speed = value
			
			time.sleep(sleep_time)
		
		self.current_speed = speed


	@property
	def debug(self):
		return self._DEBUG

	@debug.setter
	def debug(self, debug):
		''' Set if debug information shows '''
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print(self._DEBUG_INFO, "Set debug on")
			self.left_wheel.debug = True
			self.right_wheel.debug = True
			# self.pwm.debug = True
		else:
			print(self._DEBUG_INFO, "Set debug off")
			self.left_wheel.debug = False
			self.right_wheel.debug = False
			# self.pwm.debug = False

	# def ready(self):
	# 	''' Get the back wheels to the ready position. (stop) '''
	# 	self._debug_('Turn to "Ready" position')
	# 	self.left_wheel.offset = self.forward_A
	# 	self.right_wheel.offset = self.forward_B
	# 	self.stop()

	# def calibration(self):
	# 	''' Get the front wheels to the calibration position. '''
	# 	self._debug_('Turn to "Calibration" position')
	# 	self.speed = 50
	# 	self.forward()
	# 	self.cali_forward_A = self.forward_A
	# 	self.cali_forward_B = self.forward_B

	# def cali_left(self):
	# 	''' Reverse the left wheels forward direction in calibration '''
	# 	self.cali_forward_A = (1 + self.cali_forward_A) & 1
	# 	self.left_wheel.offset = self.cali_forward_A
	# 	self.forward()

	# def cali_right(self):
	# 	''' Reverse the right wheels forward direction in calibration '''
	# 	self.cali_forward_B = (1 + self.cali_forward_B) & 1
	# 	self.right_wheel.offset = self.cali_forward_B
	# 	self.forward()

	# def cali_ok(self):
	# 	''' Save the calibration value '''
	# 	self.forward_A = self.cali_forward_A
	# 	self.forward_B = self.cali_forward_B
	# 	self.db.set('forward_A', self.forward_A)
	# 	self.db.set('forward_B', self.forward_B)
	# 	self.stop()

# def test():
# 	import time
# 	back_wheels = Back_Wheels()
# 	DELAY = 0.01
# 	try:
# 		back_wheels.forward()
# 		for i in range(0, 100):
# 			back_wheels.speed = i
# 			print("Forward, speed =", i)
# 			time.sleep(DELAY)
# 		for i in range(100, 0, -1):
# 			back_wheels.speed = i
# 			print("Forward, speed =", i)
# 			time.sleep(DELAY)

# 		back_wheels.backward()
# 		for i in range(0, 100):
# 			back_wheels.speed = i
# 			print("Backward, speed =", i)
# 			time.sleep(DELAY)
# 		for i in range(100, 0, -1):
# 			back_wheels.speed = i
# 			print("Backward, speed =", i)
# 			time.sleep(DELAY)
# 	except KeyboardInterrupt:
# 		print("KeyboardInterrupt, motor stop")
# 		back_wheels.stop()
# 	finally:
# 		print("Finished, motor stop")
# 		back_wheels.stop()

# if __name__ == '__main__':
# 	test()


        


