from robo_car import RoboCar
import logging
import sys
import time

from config import Config

from camera_servos import CameraServos

def main():
    # print system info
    logging.info('Starting Car, system info: ' + sys.version)

    config = Config()
    
    with RoboCar() as car:
        car.start()

        # car.show_webcam(False)
        car.move_camera()
        # car.calibrate_steering()
        
        car.drive(config.get('car_control.initial_speed'))
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()