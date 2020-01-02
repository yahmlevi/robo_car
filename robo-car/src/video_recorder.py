import cv2
import datetime
import logging

class VideoRecorder(object):

    def __init__(self, path, screen_width, screen_height):
        logging.info('Creating a VideoRecorder...')

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_writer = cv2.VideoWriter(path, self.fourcc, 20.0, (screen_width, screen_height))

    def write(self, frame):
        self.video_writer.write(frame)

    def release(self):
        self.video_writer.release()