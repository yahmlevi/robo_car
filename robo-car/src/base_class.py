#!/usr/bin/env python
'''
**********************************************************************
* Filename    : base_class.py
* Description : 
* Update      : 
**********************************************************************
'''

from config import Config

class BaseClass(object):

	_DEBUG = False

	def __init__(self, debug):
		
		class_name = type(self).__name__ 


		self._DEBUG_INFO = 'DEBUG "{}":'.format(class_name)

		self.config = Config()
		
		self.is_debuggable = debug or class_name in self.config.get("debug")
		

	def debug(self, message):
		if self._DEBUG:
			print(self._DEBUG_INFO, message)
	
	@property
	def is_debuggable(self):
		return self._DEBUG

	@is_debuggable.setter
	def is_debuggable(self, value):
		''' Set if debug information shows '''
		if value in (True, False):
			self._DEBUG = value
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(value))

		if self._DEBUG:
			print(self._DEBUG_INFO, "Set debug on")
		else:
			print(self._DEBUG_INFO, "Set debug off")
