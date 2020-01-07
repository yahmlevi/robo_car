#!/usr/bin/env python

# from .SunFounder_PCA9685 import Servo
from steering_servo import SteeringServo
from file_db import FileDb

from base_class import BaseClass

class FrontWheelSteering(BaseClass):

	''' Front wheels control class '''
	FRONT_WHEEL_CHANNEL = 0

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "FrontWheelSteering.py":'

	def __init__(self, debug=False, db="file_db_data", bus_number=1, channel=FRONT_WHEEL_CHANNEL):

		BaseClass.__init__(self, debug)

		''' setup channels and basic stuff '''

		self.db = FileDb(db=db)
		# self._channel = channel
		self._straight_angle = 90
		self.turning_max = 45
		self._turning_offset = int(self.db.get('turning_offset', default_value=0))

		self.servo = SteeringServo(debug=debug)
		
		#  self.debug('Front wheel PWM channel: %s' % self._channel)
		self.debug('Front wheel offset value: %s ' % self.turning_offset)

		self._angle = {"left":self._min_angle, "straight":self._straight_angle, "right":self._max_angle}
		self.debug('left angle: %s, straight angle: %s, right angle: %s' % (self._angle["left"], self._angle["straight"], self._angle["right"]))

	

	def turn_left(self):
		''' Turn the front wheels left '''
		self.debug("Turn left")
		self.servo.write(self._angle["left"])

	def turn_straight(self):
		''' Turn the front wheels back straight '''
		self.debug("Turn straight")
		self.servo.write(self._angle["straight"])

	def turn_right(self):
		''' Turn the front wheels right '''
		self.debug("Turn right")
		self.servo.write(self._angle["right"])

	def turn(self, angle):
		''' Turn the front wheels to the giving angle '''
		#  self.debug("Turn to %s " % angle)
		if angle < self._angle["left"]:
			angle = self._angle["left"]
		if angle > self._angle["right"]:
			angle = self._angle["right"]

		self.servo.write(angle)
		self.debug("Turn to %s " % angle)
		
	@property
	def channel(self):
		return self._channel
	
	@channel.setter
	def channel(self, chn):
		self._channel = chn

	@property
	def turning_max(self):
		return self._turning_max

	@turning_max.setter
	def turning_max(self, angle):
		self._turning_max = angle
		self._min_angle = self._straight_angle - angle
		self._max_angle = self._straight_angle + angle
		self._angle = {"left":self._min_angle, "straight":self._straight_angle, "right":self._max_angle}

	@property
	def turning_offset(self):
		return self._turning_offset

	@turning_offset.setter
	def turning_offset(self, value):
		if not isinstance(value, int):
			raise TypeError('"turning_offset" must be "int"')
		self._turning_offset = value
		self.db.set('turning_offset', value)
		# self.servo.offset = value
		self.turn_straight()

	# @property
	# def debug(self):
	# 	return self._DEBUG
	
	# @debug.setter
	# def debug(self, debug):
	# 	''' Set if debug information shows '''
	# 	if debug in (True, False):
	# 		self._DEBUG = debug
	# 	else:
	# 		raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

	# 	if self._DEBUG:
	# 		print(self._DEBUG_INFO, "Set debug on")
	# 		print(self._DEBUG_INFO, "Set wheel debug on")
			
	# 	else:
	# 		print(self._DEBUG_INFO, "Set debug off")
	# 		print(self._DEBUG_INFO, "Set wheel debug off")

	# 	# self.servo.debug = debug

	def ready(self):
		''' Get the front wheels to the ready position. '''
		self.debug('Turn to "Ready" position')
		self.servo.offset = self.turning_offset
		self.turn_straight()

	def calibration(self):
		''' Get the front wheels to the calibration position. '''
		self.debug('Turn to "Calibration" position')
		self.turn_straight()
		self.cali_turning_offset = self.turning_offset

	def cali_left(self):
		''' Calibrate the wheels to left '''
		self.cali_turning_offset -= 1
		self.servo.offset = self.cali_turning_offset
		self.turn_straight()

	def cali_right(self):
		''' Calibrate the wheels to right '''
		self.cali_turning_offset += 1
		self.servo.offset = self.cali_turning_offset
		self.turn_straight()

	def cali_ok(self):
		''' Save the calibration value '''
		self.turning_offset = self.cali_turning_offset
		self.db.set('turning_offset', self.turning_offset)
