from publisher import Publisher
from subscriber import Subscriber

import time

topic="tsadok"

publisher = Publisher(topic=topic)
subscriber = Subscriber(topic=topic)

for i in range(1,10):
    message = "%d" % i 
    publisher.publish(message)


for i in range(1,10):
    print (subscriber.receive())


# try:
#     while True:
#         # logging.info('Pressed key %s', key)
#         print (subscriber.receive())

#         time.sleep(1)

# except KeyboardInterrupt:
#     print ("Ctrl+C was pressed ")
#     pass

