#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq

# https://stackoverflow.com/questions/4163964/python-is-it-possible-to-attach-a-console-into-a-running-process/4693529
# import pdb
# pdb.set_trace()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print ("Getting into endless loop ...")
while True:
    try:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: %s" % message)

        #  Do some 'work'
        time.sleep(1)

        #  Send reply back to client
        socket.send(b"World")
    except KeyboardInterrupt:
        print ("Interrupted")