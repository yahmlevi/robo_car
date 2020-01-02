#!/usr/bin/env python
import sys
import time

from m_dev import mDev, numMap

mdev = mDev()
def loop():	
	mdev.readReg(mdev.CMD_SONIC)
	while True:
		SonicEchoTime = mdev.readReg(mdev.CMD_SONIC)
		distance = SonicEchoTime * 17.0 / 1000.0
		print ("EchoTime: %d, Sonic: %.2f cm" % (SonicEchoTime, distance))
		time.sleep(0.001)
	
if __name__ == '__main__':
	import sys
	print ("mDev.py is starting ... ")
	#setup()
	try:
		if len(sys.argv)<2:
			print ("Parameter error: Please assign the device")
			exit() 
		print (sys.argv[0], sys.argv[1])
		if sys.argv[1] == "servo":		
			cnt = 3	
			while (cnt != 0):		
				cnt = cnt - 1
				for i in range(50, 140, 1):	
					mdev.writeReg(mdev.CMD_SERVO1, numMap(i, 0, 180, 500, 2500))
					time.sleep(0.005)
				for i in range(140,50,-1):	
					mdev.writeReg(mdev.CMD_SERVO1, numMap(i, 0, 180, 500, 2500))
					time.sleep(0.005)
			
			mdev.writeReg(mdev.CMD_SERVO1,numMap(90, 0, 180, 500, 2500))

		if sys.argv[1] == "buzzer":
			mdev.writeReg(mdev.CMD_BUZZER, 2000)
			time.sleep(3)
			mdev.writeReg(mdev.CMD_BUZZER, 0)

		if sys.argv[1] == "RGBLED":
			for i in range(0,3):
				mdev.writeReg(mdev.CMD_IO1, 0)
				mdev.writeReg(mdev.CMD_IO2, 1)
				mdev.writeReg(mdev.CMD_IO3, 1)
				time.sleep(1)
				mdev.writeReg(mdev.CMD_IO1, 1)
				mdev.writeReg(mdev.CMD_IO2, 0)
				mdev.writeReg(mdev.CMD_IO3, 1)
				time.sleep(1)
				mdev.writeReg(mdev.CMD_IO1,1)
				mdev.writeReg(mdev.CMD_IO2,1)
				mdev.writeReg(mdev.CMD_IO3,0)
				time.sleep(1)
	
			mdev.writeReg(mdev.CMD_IO1,1)
			mdev.writeReg(mdev.CMD_IO2,1)
			mdev.writeReg(mdev.CMD_IO3,1)
		
		if sys.argv[1] == "ultrasonic" or sys.argv[1] == "s":
			while True:
				print ("Sonic: ",mdev.getSonic())
				time.sleep(0.1)
		
		if sys.argv[1] == "motor":
			
			# forward
			mdev.writeReg(mdev.CMD_DIR1, 0)
			mdev.writeReg(mdev.CMD_DIR2, 0)

			min_speed = 0
			max_speed = 1000
			speed_change = 10

			sleep_time = 0.005

			# accelerate
			for i in range(0, 1000, 10):	
				mdev.writeReg(mdev.CMD_PWM1, i)
				mdev.writeReg(mdev.CMD_PWM2, i)
				time.sleep(sleep_time)
			time.sleep(1)
			for i in range(1000,0,-10):	
				mdev.writeReg(mdev.CMD_PWM1, i)
				mdev.writeReg(mdev.CMD_PWM2, i)
				time.sleep(sleep_time)
			
			# backwards
			mdev.writeReg(mdev.CMD_DIR1, 1)
			mdev.writeReg(mdev.CMD_DIR2, 1)

			# decelerate
			for i in range(0, 1000, 10):	
				mdev.writeReg(mdev.CMD_PWM1, i)
				mdev.writeReg(mdev.CMD_PWM2, i)
				time.sleep(sleep_time)
			time.sleep(1)
			for i in range(1000, 0, -10):	
				mdev.writeReg(mdev.CMD_PWM1, i)
				mdev.writeReg(mdev.CMD_PWM2, i)
				time.sleep(sleep_time)
	
	except KeyboardInterrupt:
		pass	
