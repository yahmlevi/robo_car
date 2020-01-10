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
from base_class import BaseClass

class SteeringServo(BaseClass):

	def __init__(self, debug=False):
		BaseClass.__init__(self, debug)
		
		# TODO: do we neeed lock?
		# self.lock = True

	
		self.mdev = mDev()

		self.current_angle = 90
		self.offset = 0
		self.write(90)
	
	
	def write(self, angle):
		''' Turn the servo with giving angle. '''

		# if self.lock:
		if True:
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
		self.debug('Turn angle = %d' % angle)

		adjust = False
		if adjust:
			if angle > self.current_angle:
				direction = 1
			else: 
				direction = -1

			# turn from 50 to 140 by 1 every 0.005
			for value in range(self.current_angle, angle, direction):	

				# Add the the offset value to value
				value = value + self.offset
				self.debug('Turn angle (with offset) = %d' % value)

				self.mdev.writeReg(self.mdev.CMD_SERVO1, numMap(value, 0, 180, 500, 2500))
				time.sleep(0.005)
			
			# save angle in self.current_angle for next call
			self.current_angle = angle

		else:
			value = angle + self.offset

			self.debug('Turn angle (with offset) = %d' % value)
			self.mdev.writeReg(self.mdev.CMD_SERVO1, numMap(value, 0, 180, 500, 2500))

