#!/usr/bin/env python
'''
**********************************************************************
* Filename    : CameraServos.py
* Description : 
* Update      : 
**********************************************************************
'''
import logging
import time
from freenove.m_dev import mDev, numMap
from config import Config
from base_class import BaseClass


class CameraServos(BaseClass):
	'''CameraServo driver class'''

	def __init__(self, debug=False):

		BaseClass.__init__(self, debug=debug )
		
		self.mdev = mDev()

		self.vertical = 90
		self.horizontal = 90

		self.reset()

	def reset(self):

		config = Config()
		
		# camera:
		# 	angles:
		# 		vertical: 70            # servo2
		# 		horizontal: 20          # servo3

		self.vertical = config.get('camera.angles.vertical')
		self.horizontal = config.get('camera.angles.horizontal')

		logging.info('Resetting to initial values: vertical %d, horizontal %d', self.vertical, self.horizontal)

		servo = self.mdev.CMD_SERVO2
		self.mdev.writeReg(servo, numMap(self.vertical, 0, 180, 500, 2500))

		servo = self.mdev.CMD_SERVO3
		self.mdev.writeReg(servo, numMap(self.horizontal, 0, 180, 500, 2500))

	def up(self, change = 1):
		servo = self.mdev.CMD_SERVO2
		
		self.vertical += change
		self.mdev.writeReg(servo, numMap(self.vertical, 0, 180, 500, 2500))

	def down(self, change = 1):
		servo = self.mdev.CMD_SERVO2

		self.vertical -= change
		self.mdev.writeReg(servo, numMap(self.vertical, 0, 180, 500, 2500))
	
	def left(self, change = 1):
		servo = self.mdev.CMD_SERVO3
		
		self.horizontal += change
		self.mdev.writeReg(servo, numMap(self.horizontal, 0, 180, 500, 2500))

	def right(self, change = 1):
		servo = self.mdev.CMD_SERVO3
		
		self.horizontal -= change
		self.mdev.writeReg(servo, numMap(self.horizontal, 0, 180, 500, 2500))
