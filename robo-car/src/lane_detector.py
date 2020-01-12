import cv2
import numpy as np
import logging
import math
import datetime
import sys
# import os
import yaml

from display_functions import show_image, display_lines

from base_class import BaseClass

# HandCodedLaneFollower
class LaneDetector(BaseClass):

    def __init__(self, debug=False, config=None):
        BaseClass.__init__(self, debug)

        # logging.info('Creating a LaneDetector...')
        self.debug('Creating a LaneDetector...')

    def detect(self, frame):
        return self.detect_lane(frame)

    def detect_lane(self, frame):
        self.debug('detecting lane lines...')

        ########################################################
        # Frame processing steps
        ########################################################

        # 1. Detect edges
        edges = self.detect_edges(frame)
        show_image('edges', edges)

        # 2. Leave only the region of interest (crop the upper part of the image)
        cropped_edges = self.region_of_interest(edges)
        show_image('edges cropped', cropped_edges)

        # 3. Detect line segments
        line_segments = self.detect_line_segments(cropped_edges)
        line_segment_image = display_lines(frame, line_segments)
        show_image("line segments", line_segment_image)

        # 4. Average the 'slope' (=a) and 'intercept' (=b) of the linear equation (y=a*x+b)
        #    that describe the lane line(s)
        lane_lines = self.average_slope_intercept(frame, line_segments)
        lane_lines_image = display_lines(frame, lane_lines)
        show_image("lane lines", lane_lines_image)

        return lane_lines, lane_lines_image


    def detect_edges(self, frame):
        # filter for blue lane lines
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        show_image("hsv", hsv)

        # lower_blue = np.array([30, 40, 0])
        # upper_blue = np.array([150, 255, 255])

        base_key = "image_processing.lane_detection"

        print("--------------------------------------------------")
        print(self.config.get("lower_color", base_key))
        print(self.config.get("upper_color", base_key))
        print("--------------------------------------------------")

        lower_blue = self.config.get("lower_color", base_key)
        upper_blue = self.config.get("upper_color", base_key)

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        show_image("blue mask", mask)

        # detect edges
        # edges = cv2.Canny(mask, 200, 400)
        min_val = self.config.get("canny.min_val", base_key)
        max_val = self.config.get("canny.max_val", base_key)

        edges = cv2.Canny(mask, min_val, max)

        return edges

    def detect_edges_old(self, frame):
        # filter for blue lane lines
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        show_image("hsv", hsv)
        for i in range(16):
            lower_blue = np.array([30, 16 * i, 0])
            upper_blue = np.array([150, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            show_image("blue mask Sat=%s" % (16* i), mask)


        #for i in range(16):
            #lower_blue = np.array([16 * i, 40, 50])
            #upper_blue = np.array([150, 255, 255])
            #mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # show_image("blue mask hue=%s" % (16* i), mask)

            # detect edges
        edges = cv2.Canny(mask, 200, 400)

        return edges

    def region_of_interest(self, canny):
        height, width = canny.shape
        mask = np.zeros_like(canny)

        # only focus bottom half of the screen

        polygon = np.array([[
            (0, height * 1 / 2),
            (width, height * 1 / 2),
            (width, height),
            (0, height),
        ]], np.int32)

        cv2.fillPoly(mask, polygon, 255)
        show_image("mask", mask)
        masked_image = cv2.bitwise_and(canny, mask)
        return masked_image

    def detect_line_segments(self, cropped_edges):
        # https://towardsdatascience.com/deeppicar-part-4-lane-following-via-opencv-737dd9e47c96
        # From lanes.py
        # lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap = 5)

        # GETTING environment variables
        # using get will return `None` if a key is not present rather than raise a `KeyError`
        # print(os.environ.get('KEY_THAT_MIGHT_EXIST'))

        # os.getenv is equivalent, and can also give a default value instead of `None`
        
        # rho = 1  # precision in pixel, i.e. 1 pixel

        base_key = "image_processing.lane_detection.hough_transform"
        rho = self.config.get("rho", base_key)

        # degree in radian, i.e. 1 degree
        angle = np.pi / 180             

        # minimal of votes
        min_threshold = self.config.get('min_threshold', base_key)    
        
        # 8
        min_line_length = self.config.get("min_line_length", base_key)     
        min_line_gap = 4

        # Use "Hough Line Transform" to detect lines in 'cropped_edges' image
        # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
        line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, np.array([]), minLineLength=min_line_length, maxLineGap=min_line_gap)


        if line_segments is not None:
            for line_segment in line_segments:

                self.debug('detected line_segment:')
                self.debug("%s of length %s" % (line_segment, length_of_line_segment(line_segment[0])))

        return line_segments

    def average_slope_intercept(self, frame, line_segments):
        """
        This function combines line segments into one or two lane lines
        If all line slopes are < 0: then we only have detected left lane
        If all line slopes are > 0: then we only have detected right lane
        """
        lane_lines = []
        if line_segments is None:
            # logging.info('No line_segment segments detected')
            self.debug('No line_segment segments detected')
            return lane_lines

        height, width, _ = frame.shape
        left_fit = []
        right_fit = []

        boundary = 1/3
        left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
        right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

        for line_segment in line_segments:
            for x1, y1, x2, y2 in line_segment:
                if x1 == x2:
                    # logging.info('skipping vertical line segment (slope=inf): %s' % line_segment)
                    self.debug('skipping vertical line segment (slope=inf): %s' % line_segment)
                    continue
                fit = np.polyfit((x1, x2), (y1, y2), 1)
                slope = fit[0]
                intercept = fit[1]
                if slope < 0:
                    if x1 < left_region_boundary and x2 < left_region_boundary:
                        left_fit.append((slope, intercept))
                else:
                    if x1 > right_region_boundary and x2 > right_region_boundary:
                        right_fit.append((slope, intercept))

        left_fit_average = np.average(left_fit, axis=0)
        if len(left_fit) > 0:
            lane_lines.append(make_points(frame, left_fit_average))

        right_fit_average = np.average(right_fit, axis=0)
        if len(right_fit) > 0:
            lane_lines.append(make_points(frame, right_fit_average))

        self.debug('lane lines: %s' % lane_lines)  # [[[316, 720, 484, 432]], [[1009, 720, 718, 432]]]

        return lane_lines


########################################################
# Utility Functions
########################################################

def length_of_line_segment(line):
    x1, y1, x2, y2 = line
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]


