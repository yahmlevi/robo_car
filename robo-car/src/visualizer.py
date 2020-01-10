import cv2
import platform
from threading import Thread

class Visualizer(object):
		

    def __init__(self, name="WebcamVideoVisualizer"):
        
        # initialize the thread name
        self.name = name
        
        # initialize the variable used to indicate if the thread should be stopped
        self.stopped = False

        self.title = ""
        self.frame = None
        self.frame_prev = None

    # ---------------------------------------------------
    # Support threading
    # ---------------------------------------------------

    def start(self):
        self.stopped = False

        # start the thread to read frames from the video stream
        thread = Thread(target=self.show_worker, name=self.name, args=())
        thread.daemon = True
        thread.start()
        
        return self

    # don't call this method - it's being called from start()
    def show_worker(self):
        
        # keep looping infinitely until the thread is stopped
        while True:
		    # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
                
            # otherwise, show the image
            if self.frame is not None and self.frame != self.frame_prev:
                self.frame_prev = self.frame
                cv2.imshow(self.title, self.frame)
                

    def show(self, title, frame):
        self.title = title
        self.frame = frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True        
        