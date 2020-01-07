#!/usr/bin/env python
import sys
import time

from m_dev import mDev, numMap

mdev = mDev()
			
servo = mdev.CMD_SERVO2
value = 70
mdev.writeReg(servo, numMap(value, 0, 180, 500, 2500))

servo = mdev.CMD_SERVO3
value = 20
mdev.writeReg(servo, numMap(value, 0, 180, 500, 2500))

	