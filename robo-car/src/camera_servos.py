#!/usr/bin/env python
'''
**********************************************************************
* Filename    : CameraServos.py
* Description : 
* Update      : 
**********************************************************************
'''
import time
from freenove.m_dev import mDev, numMap
from config import Config
from base_class import BaseClass

class CameraServos(BaseClass):
	'''CameraServo driver class'''

	def __init__(self, debug=False):

		BaseClass.__init__(self, debug=debug )
		
		self.mdev = mDev()
		self.reset()

	def reset(self):

		config = Config()

		# camera:
		# 	angles:
		# 		vertical: 70            # servo2
		# 		horizontal: 20          # servo3

		servo = self.mdev.CMD_SERVO2
		value = config.get_dict()['camera']['angles']['vertical']
		self.mdev.writeReg(servo, numMap(value, 0, 180, 500, 2500))

		servo = self.mdev.CMD_SERVO3
		value = config.get_dict()['camera']['angles']['horizontal']
		self.mdev.writeReg(servo, numMap(value, 0, 180, 500, 2500))

	def up_down(self, angle):
		servo = mdev.CMD_SERVO2

		# TODO: use offset (from init)
		mdev.writeReg(servo, numMap(angle, 0, 180, 500, 2500))
	
	def left_right(self, angle):
		servo = mdev.CMD_SERVO3

		# TODO: use offset (from init)
		mdev.writeReg(servo, numMap(angle, 0, 180, 500, 2500))
