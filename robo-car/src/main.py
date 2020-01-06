from robo_car import RoboCar
import logging
import sys
import time

def main():
    # print system info
    logging.info('Starting Car, system info: ' + sys.version)
    
    with RoboCar() as car:
        # car.drive(40)
        car.start()
        car.drive(500)
        time.sleep(2)
        car.drive(0)
        


    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()