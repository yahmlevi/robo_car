#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
#connects via localhost (change name to relevent one)
socket.connect("tcp://localhost:5555")


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