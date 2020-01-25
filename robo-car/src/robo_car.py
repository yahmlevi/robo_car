import logging

# https://github.com/t1m0thyj/picar
# import picar

import cv2
import datetime
import time

from lane_follower import LaneFollower
from object_detection import ObjectsOnRoadProcessor

import platform

from display_functions import show_image

from front_wheel_steering import FrontWheelSteering
from front_wheel_drive import FrontWheelDrive
from video_recorder import VideoRecorder

from camera import Camera
from visualizer import Visualizer
from config import Config

from base_class import BaseClass

_SHOW_IMAGE = True

class RoboCar(BaseClass):

    __INITIAL_SPEED = 0
    __SCREEN_WIDTH = 320
    __SCREEN_HEIGHT = 240

    def __init__(self):
        BaseClass.__init__(self, debug=False)
        
        """ Init camera and wheels"""
        logging.info('Creating a DeepPiCar...')

        # picar.setup()

        logging.debug('Set up camera')

        # TODO: why use -1
        # self.camera = cv2.VideoCapture(-1)
        # self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # self.camera = self.get_camera()
        # self.camera.set(3, self.__SCREEN_WIDTH)
        # self.camera.set(4, self.__SCREEN_HEIGHT)

        # TODO: implement Camera class in camera.py
        self.camera = Camera(self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT)
        self.visualizer = Visualizer()

        # self.pan_servo = picar.Servo.Servo(1)
        # self.pan_servo.offset = -30  # calibrate servo to center
        # self.pan_servo.write(90)

        # self.tilt_servo = picar.Servo.Servo(2)
        # self.tilt_servo.offset = 20  # calibrate servo to center
        # self.tilt_servo.write(90)

        # logging.debug('Set up back wheels')
        # self.back_wheels = picar.back_wheels.Back_Wheels()
        # self.back_wheels.speed = 0  # Speed Range is 0 (stop) - 100 (fastest)

        logging.debug('Set up fron wheel drive')
        self.front_wheel_drive = FrontWheelDrive()
        self.front_wheel_drive.speed = 0  # Speed Range is 0 (stop) - 100 (fastest)

        logging.debug('Set up front wheel steering')
        self.front_wheel_steering = FrontWheelSteering()
        
        # self.front_wheel_steering.turning_offset = -25  # calibrate servo to center

        temp = self.config.get("front_wheel_steering.turning_offset")
        logging.debug('Turning offset %d' % temp)
        self.front_wheel_steering.turning_offset = temp
        self.front_wheel_steering.turn(90)              # Steering Range is 45 (left), 90 (center), 135 (right)

        # HandCodedLaneFollower(self)

        self.lane_follower = LaneFollower(self)
        # lane_follower = DeepLearningLaneFollower()

        self.traffic_sign_processor = ObjectsOnRoadProcessor(self)

        # ----------------------
        # self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        date_str = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        # self.video_orig = self.create_video_recorder('../data/tmp/car_video%s.avi' % date_str)
        # self.video_lane = self.create_video_recorder('../data/tmp/car_video_lane%s.avi' % date_str)
        # self.video_objs = self.create_video_recorder('../data/tmp/car_video_objs%s.avi' % date_str)

        self.video_orig = VideoRecorder('videos/car_video%s.avi' % date_str, self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT)
        self.video_lane = VideoRecorder('videos/car_video_lane%s.avi' % date_str, self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT)
        self.video_objs = VideoRecorder('videos/car_video_objs%s.avi' % date_str, self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT)

        logging.info('Created a RoboCar')


    # def create_video_recorder(self, path):
    #     return cv2.VideoWriter(path, self.fourcc, 20.0, (self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))

    def __enter__(self):
        """ Entering a with statement """
        return self

    def __exit__(self, _type, value, traceback):
        """ Exit a with statement"""
        if traceback is not None:
            # Exception occurred:
            logging.error('Exiting with statement with exception %s' % traceback)

        self.cleanup()

    def cleanup(self):
        """ Reset the hardware"""
        logging.info('Stopping the car, resetting hardware.')
        # self.back_wheels.speed = 0
        # self.front_wheels.turn(90)
        
        self.camera.release()

        self.video_orig.release()
        self.video_lane.release()
        self.video_objs.release()

        cv2.destroyAllWindows()

    def get_camera(self):
        if platform.machine() == "AMD64":
            # https://stackoverflow.com/questions/52043671/opencv-capturing-imagem-with-black-side-bars?rq=1
            return cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            return cv2.VideoCapture(0)

    def start(self):
        # start the camera thread
        self.camera.start()
        self.visualizer.start()
    
    # def drive(self, self_drive=False, speed=__INITIAL_SPEED, forward=True):
    def drive(self, speed=__INITIAL_SPEED, forward=True):
        """ Main entrypoint of the car, and put it in drive mode
        Keyword arguments:
        speed -- speed of back wheel, range is 0 (stop) - 100 (fastest)
        """

        logging.info('Starting to drive at speed %s...' % speed)
        
        self.front_wheel_drive.forward()
        # self.front_wheel_drive.speed = speed

        display_video =  "lane_lines" in self.config.get("display")
        record = False

        i = 0
        while self.camera.isOpened():
            # _, image_lane = self.camera.read()
            image_lane = self.camera.read()
            
            image_objs = image_lane.copy()
            i += 1
            
            if record:
                self.video_orig.write(image_lane)

            # image_objs = self.process_objects_on_road(image_objs)
            image_objs = self.traffic_sign_processor.process_objects_on_road(image_objs)
            
            # self.video_objs.write(image_objs)
            show_image('Detected Objects', image_objs, show=display_video)

            image_lane = self.lane_follower.follow_lane(image_lane)

            # wait 100/20 = seconds before driving
            if image_lane is not None and i >= 100: 
                self.front_wheel_drive.speed = speed

            # if i >= 200: 
            #     self.front_wheel_drive.speed = speed

            if record:
                self.video_lane.write(image_lane)

            show_image('lane_lines', image_lane, show=display_video)
            # self.visualizer.show(title = "Lane Lines", frame = image_lane)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cleanup()
                break

   


    def show_webcam(self, mirror=False):
        scale = 1

        while self.camera.isOpened():
            logging.info('Camera is opened')

            # ret_val, image = self.camera.read()
            image = self.camera.read()

            if mirror: 
                image = cv2.flip(image, 1)

            #get the webcam size
            height, width, channels = image.shape

            #prepare the crop
            centerX, centerY = int(height / 2), int(width / 2)
            radiusX, radiusY = int(scale * height / 100), int(scale * width / 100)

            minX, maxX = centerX - radiusX, centerX + radiusX
            minY, maxY = centerY - radiusY, centerY + radiusY

            logging.info('Cropping image to width %d and height %s', width, height)
            cropped = image[minX:maxX, minY:maxY]
            resized_cropped = cv2.resize(cropped, (width, height)) 
            
            cv2.imshow('my webcam', resized_cropped)

            key = cv2.waitKey(1)
            logging.info('Pressed key %s', key)

            if key == 27: 
                break  # esc to quit

            #add + or - 5 % to zoom

            # right arrow key
            if key == 83: 
                scale += 5  # +5

            # left arrow key
            if key == 81: 
                scale -= 5  # -5

        cv2.destroyAllWindows()


    def move_camera(self):
        from camera_servos import CameraServos

        # TODO: move this to more appropriate place
        camera_servos = CameraServos()

        while self.camera.isOpened():
            # ret_val, image = self.camera.read()
            image = self.camera.read()
            
            # logging.info('Move camera %d and height %s', width, height)
            cv2.imshow('Car Cam', image)

            key = cv2.waitKey(1)

            if key == 27: 
                break  # esc to quit

            if cv2.waitKey(1) & 0xFF == ord('r'):
                logging.info('Resetting to initial values')
                camera_servos.reset()
            
            # right arrow key
            if key == 83: 
                logging.info('Pressed key %s', key)
                camera_servos.right()

            # left arrow key
            if key == 81: 
                logging.info('Pressed key %s', key)
                camera_servos.left()

            # up arrow key
            if key == 82: 
                logging.info('Pressed key %s', key)
                camera_servos.up()

            # down arrow key
            if key == 84: 
                logging.info('Pressed key %s', key)
                camera_servos.down()
            
        cv2.destroyAllWindows()


    def calibrate_steering(self):
        from front_wheel_steering import FrontWheelSteering
        
        steering = FrontWheelSteering()

        # 1st - turn to 90
        steering.turn_straight()
        current_angle = 90

        logging.info('Front wheel current steering angle: %s' % current_angle)
        
        while self.camera.isOpened():
            # ret_val, image = self.camera.read()
            image = self.camera.read()
            cv2.imshow('Car Cam', image)
            
            key = cv2.waitKey(1)
            if key == 27: 
                break  # esc to quit

            if cv2.waitKey(1) & 0xFF == ord('r'):
                logging.info('Resetting to initial values')
                # steering.reset()

            # right arrow key
            if key == 83: 
                logging.info('Pressed key %s', key)
                current_angle += 1
                steering.turn(current_angle)

                logging.info('Front wheel current steering angle: %s' % current_angle)
                logging.info('Front wheel current turning offset: %s' % steering.turning_offset)

            # left arrow key
            if key == 81: 
                logging.info('Pressed key %s', key)
                current_angle -= 1
                steering.turn(current_angle)

                logging.info('Front wheel current steering angle: %s' % current_angle)
                logging.info('Front wheel current turning offset: %s' % steering.turning_offset)

            # up arrow key 
            if key == 82: 
                logging.info('Pressed key %s', key)
                steering.turn_straight()
                current_angle = 90

                logging.info('Front wheel current steering angle: %s' % current_angle)
                logging.info('Front wheel current turning offset: %s' % steering.turning_offset)

            

        cv2.destroyAllWindows()
            
