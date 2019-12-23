# FROM schickling/opencv:latest
# FROM mohaseeb/raspberrypi3-python-opencv

FROM jjanzic/docker-python3-opencv
WORKDIR /app

RUN apt-get update && \
    apt-get install -y net-tools nano

    # libgtk2.0-dev pkg-config
    # apt-get install libqt4-dev

RUN pip install --upgrade pip opencv-contrib-python zmq imutils Flask


# Troubleshooting "libdc1394 error: Failed to initialize libdc1394"
# -------------------------------------------------------------------
# https://hub.docker.com/r/ekazakov/python-opencv
# https://stackoverflow.com/questions/29274638/opencv-libdc1394-error-failed-to-initialize-libdc1394
#
# Solution:
# -------------------------------------------------------------------
# ENTRYPOINT ln -s /dev/null /dev/raw1394 && /bin/bash