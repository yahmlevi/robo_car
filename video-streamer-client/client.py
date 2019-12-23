# USAGE
# python client.py --server-ip server-ip
# python client.py --server-ip localhost

from imutils.video import VideoStream

# import imagezmq
# from imagezmq import ImageSender, ImageHub
import imagezmq.imagezmq as imagezmq

import cv2
import argparse
import socket
import time
import platform

def get_camera():
	if platform.machine() == "AMD64":
		# https://stackoverflow.com/questions/52043671/opencv-capturing-imagem-with-black-side-bars?rq=1
		return cv2.VideoCapture(0, cv2.CAP_DSHOW)
	else:
		return cv2.VideoCapture(0)

def main():
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
	#vs = VideoStream(src=0).start()
	#print ("[INFO] acquired VideoStream")
	vs = get_camera()

	time.sleep(2.0)
	
	try:
		#while True:
		while (vs.isOpened()):
			# read the frame from the camera and send it to the server
			print ("Reading from VideoStream")
			#frame = vs.read()
			_, frame = vs.read()

			#cv2.imshow("frame", frame)
			
			# print ("Sending frame to {}".format(rpiName))
			sender.send_image(rpiName, frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
                # When everything done, release the capture

	except KeyboardInterrupt:
		print ("Interrupted")
	finally: 
		vs.release()
		cv2.destroyAllWindows()


def capture_video_from_camera():
    print ("Running 'capture_video_from_camera")
    
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap = get_camera()
    try:
        while(cap.isOpened()):
            print ("Camera is open")

            # Capture frame-by-frame
            ret, frame = cap.read()

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the resulting frame
            cv2.imshow('frame', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                # When everything done, release the capture

    except KeyboardInterrupt:
        print ("Interrupted")
    finally: 
        cap.release()
        cv2.destroyAllWindows()



main()