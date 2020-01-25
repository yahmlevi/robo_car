import cv2
import logging
import datetime
import time
import edgetpu.detection.engine
from PIL import Image
import platform
# from traffic_objects import *
from objects_on_road_processor import ObjectsOnRoadProcessor

_SHOW_IMAGE = True


############################
# Utility Functions
############################
def show_image(title, frame, show=_SHOW_IMAGE):
    if show:
        cv2.imshow(title, frame)


############################
# Test Functions
############################
def test_photo(file):
    object_processor = ObjectsOnRoadProcessor()
    frame = cv2.imread(file)
    combo_image = object_processor.process_objects_on_road(frame)
    show_image('Detected Objects', combo_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def test_stop_sign():
    # this simulates a car at stop sign
    object_processor = ObjectsOnRoadProcessor()

    stop_sign_file = './tests/data/objects/stop_sign.jpg'
    green_light_file = './tests/data/objects/green_light.jpg'

    frame = cv2.imread(stop_sign_file)
    combo_image = object_processor.process_objects_on_road(frame)
    show_image('Stop 1', combo_image)
    time.sleep(1)
    frame = cv2.imread(stop_sign_file)
    combo_image = object_processor.process_objects_on_road(frame)
    show_image('Stop 2', combo_image)
    time.sleep(2)
    frame = cv2.imread(stop_sign_file)
    combo_image = object_processor.process_objects_on_road(frame)
    show_image('Stop 3', combo_image)
    time.sleep(1)
    frame = cv2.imread(green_light_file)
    combo_image = object_processor.process_objects_on_road(frame)
    show_image('Stop 4', combo_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def test_camera():
    print ("")
    print ("Testing camera")
    print ("=============================================")

    object_processor = ObjectsOnRoadProcessor()

    if platform.machine() == "AMD64":
        # https://stackoverflow.com/questions/52043671/opencv-capturing-imagem-with-black-side-bars?rq=1
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(0)

    # video_file
    # video_file_extension

    # video_type = cv2.VideoWriter_fourcc(*'XVID')
    # date_str = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    # video_overlay = cv2.VideoWriter("%s_overlay_%s.%s" % (video_file, date_str, video_file_extension), video_type, 20.0, (320, 240))
    try:
        i = 0
        while cap.isOpened():
            _, frame = cap.read()
            # cv2.imwrite("%s_%03d.png" % (video_file, i), frame)

            combo_image = object_processor.process_objects_on_road(frame)
            # cv2.imwrite("%s_overlay_%03d.png" % (video_file, i), combo_image)
            # video_overlay.write(combo_image)

            cv2.imshow("Detected Objects", combo_image)

            i += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        # video_overlay.release()
        cv2.destroyAllWindows()

def test_video(video_file, video_file_extension):
    print ("")
    print ("Testing video")
    print ("=============================================")

    object_processor = ObjectsOnRoadProcessor()
    cap = cv2.VideoCapture(video_file + '.' + video_file_extension)

    # skip first second of video.
    for i in range(3):
        _, frame = cap.read()

    video_type = cv2.VideoWriter_fourcc(*'XVID')
    date_str = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    video_overlay = cv2.VideoWriter("%s_overlay_%s.%s" % (video_file, date_str, video_file_extension), video_type, 20.0, (320, 240))
    try:
        i = 0
        while cap.isOpened():
            _, frame = cap.read()
            cv2.imwrite("%s_%03d.png" % (video_file, i), frame)

            combo_image = object_processor.process_objects_on_road(frame)
            cv2.imwrite("%s_overlay_%03d.png" % (video_file, i), combo_image)
            video_overlay.write(combo_image)

            cv2.imshow("Detected Objects", combo_image)

            i += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        video_overlay.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s:%(asctime)s: %(message)s')
    logging.basicConfig(level=logging.INFO, format='%(levelname)-5s:%(asctime)s: %(message)s')

    test_camera()
    test_video("./tests/data/traffic_sign_detection_pov", "mp4")

    # These processors contains no state
    test_photo('./tests/data/objects/red_light.jpg')
    test_photo('./tests/data/objects/person.jpg')
    test_photo('./tests/data/objects/limit_40.jpg')
    test_photo('./tests/data/objects/limit_25.jpg')
    test_photo('./tests/data/objects/green_light.jpg')
    test_photo('./tests/data/objects/no_obj.jpg')

    # test stop sign, which carries state
    test_stop_sign()

