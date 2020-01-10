import cv2
import platform
from threading import Thread

class Camera(object):
		

    def __init__(self, screen_width, screen_height, name="WebcamVideoStream"):
        if platform.machine() == "AMD64":
            # https://stackoverflow.com/questions/52043671/opencv-capturing-imagem-with-black-side-bars?rq=1
            self.camera_obj = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            self.camera_obj = cv2.VideoCapture(0)

        self.camera_obj.set(3, screen_width)
        self.camera_obj.set(4, screen_height)

        # initialize the video camera stream and read the first frame from the stream
        (self.grabbed, self.frame) = self.camera_obj.read()
        
        # initialize the thread name
        self.name = name
        
        # initialize the variable used to indicate if the thread should be stopped
        self.stopped = False

    def isOpened(self):
        return self.camera_obj.isOpened()

    # def read (self):
    #     return self.camera_obj.read()

    def release(self):
        self.camera_obj.release()

    # ---------------------------------------------------
    # Support threading
    # ---------------------------------------------------

    def start(self):
        self.stopped = False

        # start the thread to read frames from the video stream
        thread = Thread(target=self.update, name=self.name, args=())
        thread.daemon = True
        thread.start()
        
        return self

    # don't call this method - it's being called from start()
    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
		    # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.camera_obj.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True        
        