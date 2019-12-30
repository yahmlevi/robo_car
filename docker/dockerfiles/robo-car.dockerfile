# FROM schickling/opencv:latest
# FROM mohaseeb/raspberrypi3-python-opencv
FROM yahmlevi/robo-car:base-rpi

WORKDIR /app

COPY video-streamer-client/src /app
COPY robo-car/src /app

# troubleshooting: "libdc1394 error: Failed to initialize libdc1394"
# https://hub.docker.com/r/ekazakov/python-opencv
# https://stackoverflow.com/questions/29274638/opencv-libdc1394-error-failed-to-initialize-libdc1394

ENTRYPOINT ln -s /dev/null /dev/raw1394 && /bin/bash
