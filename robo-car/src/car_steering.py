import cv2
import numpy as np
import logging
import math
import datetime
import sys

from display_functions import show_image, display_heading_line

class CarSteering(object):

    def __init__(self, car=None):
        logging.info('Creating a CarSteering...')

        self.car = car
        self.curr_steering_angle = 90

    def steer(self, frame, lane_lines):
        logging.debug('steering...')
        if len(lane_lines) == 0:
            logging.error('No lane lines detected, nothing to do.')
            return frame

        new_steering_angle = self.compute_steering_angle(frame, lane_lines)
        self.curr_steering_angle = self.stabilize_steering_angle(self.curr_steering_angle, new_steering_angle, len(lane_lines))

        # -------------------------------------------------------
        if self.car is not None:
            # self.car.front_wheel_steering.turn(self.curr_steering_angle)
            inverse_angle = 180 - self.curr_steering_angle
            self.car.front_wheel_steering.turn(inverse_angle)

        # TODO: use publisher instead of calling car.front_wheels dierctly
        # publish self.curr_steering_angle to `steering` queue
        # -------------------------------------------------------

        curr_heading_image = display_heading_line(frame, self.curr_steering_angle)
        show_image("heading", curr_heading_image)

        return curr_heading_image


    def compute_steering_angle(self, frame, lane_lines):
        """ Find the steering angle based on lane line coordinate
            We assume that camera is calibrated to point to dead center
        """
        if len(lane_lines) == 0:
            logging.info('No lane lines detected, do nothing')
            return -90

        height, width, _ = frame.shape
        if len(lane_lines) == 1:
            logging.debug('Only detected one lane line, just follow it. %s' % lane_lines[0])
            x1, _, x2, _ = lane_lines[0][0]
            x_offset = x2 - x1
        else:
            _, _, left_x2, _ = lane_lines[0][0]
            _, _, right_x2, _ = lane_lines[1][0]

            # Meanings:
            # ------------------------------------------
            #  0.00: car is pointing to center, 
            # -0.03: car is centered to left, 
            # +0.03: car is pointing to right
            # camera_mid_offset_percent = 0.02 
            camera_mid_offset_percent = 0 

            mid = int(width / 2 * (1 + camera_mid_offset_percent))
            x_offset = (left_x2 + right_x2) / 2 - mid

        # find the steering angle, which is 
        # the angle between the navigation direction to the end of center line
        y_offset = int(height / 2)

        angle_to_mid_radian = math.atan(x_offset / y_offset)  # angle (in radians) to center vertical line
        angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  # angle (in degrees) to center vertical line
        
        steering_angle = angle_to_mid_deg + 90  # this is the steering angle needed by picar front wheel

        logging.debug('new steering angle: %s' % steering_angle)
        return steering_angle


    def stabilize_steering_angle(self, curr_steering_angle, new_steering_angle, num_of_lane_lines, max_angle_deviation_two_lines=5, max_angle_deviation_one_lane=1):
        """
        Using last steering angle to stabilize the steering angle
        This can be improved to use last N angles, etc
        if new angle is too different from current angle, only turn by max_angle_deviation degrees
        """
        if num_of_lane_lines == 2 :
            # if both lane lines detected, then we can deviate more
            max_angle_deviation = max_angle_deviation_two_lines
        else :
            # if only one lane detected, don't deviate too much
            max_angle_deviation = max_angle_deviation_one_lane
        
        angle_deviation = new_steering_angle - curr_steering_angle
        if abs(angle_deviation) > max_angle_deviation:
            stabilized_steering_angle = int(curr_steering_angle
                                            + max_angle_deviation * angle_deviation / abs(angle_deviation))
        else:
            stabilized_steering_angle = new_steering_angle
        
        logging.info('Proposed angle: %s, stabilized angle: %s' % (new_steering_angle, stabilized_steering_angle))
        return stabilized_steering_angle
