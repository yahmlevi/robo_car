#!/usr/bin/env python
'''
**********************************************************************
* Filename    : SteeringServo.py
* Description : Driver module for steering servo, with Freenove shield
* Update      : 
**********************************************************************
'''
import time
from freenove.m_dev import mDev, numMap
# import m_dev

class SteeringServo(object):

	'''SteeringServo driver class'''
	_FREQUENCY = 60 

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "SteeringServo.py":'

	def __init__(self, debug=_DEBUG):
		
		self.debug = debug
		self._debug_("Debug on")
		
		self.lock = True

		# TODO: How do we use it (in write())?
		self.frequency = self._FREQUENCY

		self.mdev = mDev()

		self.current_angle = 90
		self.write(90)
	
	def _debug_(self, message):
		if self._DEBUG:
			print(self._DEBUG_INFO, message)

	@property
	def frequency(self):
		return self._frequency

	@frequency.setter
	def frequency(self, value):
		self._frequency = value
		# self.pwm.frequency = value

	def write(self, angle):
		''' Turn the servo with giving angle. '''

		if self.lock:
			if angle > 180:
				angle = 180
			if angle < 0:
				angle = 0
		else:
			if angle < 0 or angle > 180:
				raise ValueError("Servo \"{0}\" turn angle \"{1}\" is not in (0, 180).".format(self.channel, angle))
		
		# val = self._angle_to_analog(angle)
		# val += self.offset
		# self.pwm.write(self.channel, 0, val)
		self._debug_('Turn angle = %d' % angle)

		if angle > self.current_angle:
			direction = 1
		else: 
			direction = -1

		# turn from 50 to 140 by 1 every 0.005
		for value in range(self.current_angle, angle, direction):	
			self.mdev.writeReg(self.mdev.CMD_SERVO1, numMap(value, 0, 180, 500, 2500))
			time.sleep(0.005)
		
		# save angle in self.current_angle for next call
		self.current_angle = angle


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
		else:
			print(self._DEBUG_INFO, "Set debug off")

