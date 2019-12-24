from robo_car import RoboCar
import logging
import sys

def main():
    # print system info
    logging.info('Starting Car, system info: ' + sys.version)
    
    with RoboCar() as car:
        car.drive(40)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()