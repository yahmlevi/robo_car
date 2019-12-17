import cv2
import numpy as np
import logging
import math
import datetime
import sys

from car_steering import RoboCarSteering
from display_functions import show_image, display_lines
from lane_detector import LaneDetector

# HandCodedLaneFollower
class LaneFollower(object):

    def __init__(self, car=None):
        logging.info('Creating a LaneFollower...')
        self.car = car

        self.steering = RoboCarSteering(car)
        self.lane_detector = LaneDetector(car)

    def follow_lane(self, frame):
        # Main entry point of the lane follower
        show_image("orig", frame)

        #lane_lines, frame = detect_lane(frame)
        lane_lines, frame = self.lane_detector.detect(frame)

        # final_frame = self.steer(frame, lane_lines)
        final_frame = self.steering.steer(frame, lane_lines)

        return final_frame

