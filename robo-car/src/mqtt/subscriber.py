import logging
import paho.mqtt.client as mqtt

class Subscriber(object):

    # "test.mosquitto.org"

    def __init__(self, broker_host = "broker.hivemq.com", topics = []):
        logging.debug('Creating a mqtt client...')
        
        self.broker_host = broker_host
        self.topics = topics

        #
        # Create an MQTT client and attach on_connect and on_message routines to it.
        #
        self.client = mqtt.Client()
        
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    #
    # The callback for when the client receives a CONNACK response from the server.
    #
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
    
        # Subscribing in on_connect() - if we lose the connection and reconnect then subscriptions will be renewed.
        
        # self.client.subscribe("CoreElectronics/test")
        # self.client.subscribe("CoreElectronics/topic")

        for topic in self.topics:
            self.client.subscribe(topic)
    
    #
    # The callback for when a PUBLISH message is received from the server.
    #
    def on_message(self, client, userdata, msg):
        
        print(msg.topic + " " + str(msg.payload))

        if msg.payload == b"Hello":
            print("Received message #1, do something")
            # Do something

        if msg.payload == b"World!":
            print("Received message #2, do something else")
            # Do something else
    
    def connect(self):
        
        self.client.connect(self.broker_host, 1883, 60)
    
    #
    # Start looping
    #
    def start (self):

        # Process network traffic and dispatch callbacks. This will also handle
        # reconnecting. Check the documentation at
        # https://github.com/eclipse/paho.mqtt.python
        # for information on how to use other loop*() functions
        self.client.loop_forever()

    def subscribe(self, topic):
        logging.debug("Subscribing topic %s" % topic)

        self.client.subscribe(topic)