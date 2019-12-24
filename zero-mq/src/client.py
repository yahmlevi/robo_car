#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server ~/.docker/cli-plugins/docker-buildx build --platform=linux/arm64 --tag yahmlevi/opencv:arm64 --file opencv.dockerfile -o type=image ., expects "World" back
#

import zmq
import os

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)

# connects via localhost (change name to relevent one)
# socket.connect("tcp://localhost:5555")

server_hostname = os.getenv("SERVER_HOSTNAME") 
print("Connecting to hello world server at tcp://{}:5555".format(server_hostname))
socket.connect("tcp://{}:5555".format(server_hostname))

#  Do 10 requests, waiting each time for a response
for request in range(11):
    try:
        print("Sending request %s …" % request)
        socket.send(b"Hello from YAHM")

        #  Get the reply.
        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))
    except KeyboardInterrupt:
            print ("Interrupted")