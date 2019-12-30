import cv2
import platform

class Camera(object):

    def __init__(self, screen_width, screen_height):
        if platform.machine() == "AMD64":
            # https://stackoverflow.com/questions/52043671/opencv-capturing-imagem-with-black-side-bars?rq=1
            self.camera_obj = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            self.camera_obj = cv2.VideoCapture(0)

        self.camera_obj.set(3, screen_width)
        self.camera_obj.set(4, screen_height)

    def isOpened(self):
        return self.camera_obj.isOpened()

    def read (self):
        return self.camera_obj.read()

    def release(self):
        self.camera_obj.release()
        
