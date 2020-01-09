import zmq
import random
import sys
import time

# https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pubsub.html

class Subscriber(object):
    
    def __init__(self, topic=None):
        super().__init__()

        self.topic = topic
        self.port = "5554"

        # Socket to talk to server
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        # topic filter
        if topic is not None:
            # self.socket.setsockopt(zmq.SUBSCRIBE, self.topic)
            self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
            

        # self.socket.bind("tcp://*:%s" % self.port)
        self.socket.connect ("tcp://localhost:%s" % self.port)

    def subscribe(self, topic):
        pass

    def receive(self):
        if self.topic is not None:
            # self.socket.setsockopt(zmq.SUBSCRIBE, self.topic)
            self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)

        print ("Trying to receive")
        data = self.socket.recv()

        # setting the maxsplit parameter to 1, will return a list with 2 elements
        # topic, message = data.split(":", 1)
        topic, message = data.split()

        return message

        