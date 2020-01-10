import zmq
import sys
import logging

# https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pubsub.html

class Publisher(object):

    def __init__(self, topic):
        super().__init__()

        self.topic = topic
        self.port = "5554"

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % self.port)

    def publish(self, message):
        logging.info ("published '%s' to topic '%s'" % (message, self.topic))
        
        self.socket.send(("%s %s" % (self.topic, message)).encode('utf-8'))
        # self.socket.send_string("%s %s" % (self.topic, message))


