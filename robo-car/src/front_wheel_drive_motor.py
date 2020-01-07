#!/usr/bin/env python
'''
**********************************************************************
* Filename    : SteeringServo.py
* Description : Driver module for steering servo, with Freenove shield
* Update      : 
**********************************************************************
'''
import time
from freenove.m_dev import mDev
from base_class import BaseClass

class Motor(BaseClass):

	'''SteeringServo driver class'''
	_FREQUENCY = 60 

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "Motor.py":'

	def __init__(self, debug=False, motor = "", device=None):
		BaseClass.__init__(self, debug)
		
		self.mdev = device

		if motor == "LEFT": 
			self.dir_command = self.mdev.CMD_DIR1
			self.pwm_command = self.mdev.CMD_PWM1
		else:
			self.dir_command = self.mdev.CMD_DIR2
			self.pwm_command = self.mdev.CMD_PWM2
		
		# self.lock = True
		
		self.current_speed = 0
		self.speed = 0
	

	def forward(self):
		''' Move wheel forward '''
		self.mdev.writeReg(self.dir_command, 0)
		self.debug('Running forward')

	def backward(self):
		''' Move wheel backward '''
		self.mdev.writeReg(self.dir_command, 1)
		self.debug('Running backward')

	def stop(self):
		''' Stop wheel '''
		# self.left_wheel.stop()
		# self.right_wheel.stop()
		self.debug('Stop')

	
	@property
	def speed(self, speed):
		return self._speed

	@speed.setter
	def speed(self, speed):
		self._speed = speed
		
		''' Set moving speed '''
		self.debug('Set speed to %s' % self._speed)

		self.mdev.writeReg(self.pwm_command, speed)

		# min_speed = 0
		# max_speed = 1000
		# speed_change = 10

		# # sleep_time = 0.005
		# sleep_time = 0.005

		# # TODO: accelerate & decelerate
		# change = 10
		# if speed > self.current_speed: 
		# 	change = 10
		# else:
		# 	change = -10

		# # for value in range(self.current_speed, speed, change):	
		# for value in range(0, speed, change):	
		# 	self.debug('Changing speed to %s' % value)
		# 	# self.mdev.writeReg(self.pwm_command, value)
		# 	self.mdev.writeReg(mdev.CMD_PWM1, value)
		# 	self.mdev.writeReg(mdev.CMD_PWM2, value)
		# 	time.sleep(sleep_time)

		# self.current_speed = speed
