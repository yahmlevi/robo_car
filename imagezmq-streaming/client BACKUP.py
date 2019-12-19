# USAGE
# python client.py --server-ip SERVER_IP

from imutils.video import VideoStream

# import imagezmq
# from imagezmq import ImageSender, ImageHub
import imagezmq.imagezmq as imagezmq

import cv2
import argparse
import socket
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True, help="ip address of the server to which the client will connect")
args = vars(ap.parse_args())

# initialize the ImageSender object with the socket address of the server
sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(args["server_ip"]))

# get the host name, initialize the video stream, and allow the camera sensor to warm-up
rpiName = socket.gethostname()
print("[INFO] rpiName is {}".format(rpiName))

# vs = VideoStream(usePiCamera=True).start()
vs = VideoStream(src=0).start()
print ("[INFO] acquired VideoStream")

time.sleep(2.0)
 
while True:

	# read the frame from the camera and send it to the server
	print ("Reading from VideoStream")
	frame = vs.read()

	#cv2.imshow("frame", frame)
	
	print ("Sending frame to {}".format(rpiName))
	sender.send_image(rpiName, frame)