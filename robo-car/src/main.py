from robo_car import RoboCar
import logging
import sys
import time
import yaml

from config import Config

from camera_servos import CameraServos

def main():
    # print system info
    logging.info('Starting Car, system info: ' + sys.version)

    config = Config()
    
    with RoboCar() as car:
        # car.show_webcam(False)
        car.move_camera()
        car.start()
        car.drive(config.get_dict()['car_control']['initial_speed'])
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()