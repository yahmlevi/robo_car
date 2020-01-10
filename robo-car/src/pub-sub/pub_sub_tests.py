from publisher import Publisher
from subscriber import Subscriber

from threading import Thread

import time




def publish_worker():
    topic="tsadok"
    publisher = Publisher(topic=topic)

    for i in range(1,10):
        message = "%d" % i 
        publisher.publish(message)

        time.sleep(0.5)

    publisher.publish("END")


def subscribe_worker():
    topic="tsadok"
    subscriber = Subscriber(topic=topic)

    fail_tries = 0

    message = ""
    while message != b'END':
        message = subscriber.receive()
        if message is not None:
            print (message)
        else: 
            fail_tries += 1

    print ("Fail tries %d" % fail_tries)



def main():
    # http://zguide.zeromq.org/py:espresso

    p_thread = Thread(target=publish_worker)
    s_thread = Thread(target=subscribe_worker)

    
    s_thread.start()
    p_thread.start()


# run main
main()


# try:
#     while True:
#         # logging.info('Pressed key %s', key)
#         print (subscriber.receive())

#         time.sleep(1)

# except KeyboardInterrupt:
#     print ("Ctrl+C was pressed ")
#     pass

