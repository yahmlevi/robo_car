# FROM schickling/opencv:latest
# FROM mohaseeb/raspberrypi3-python-opencv
# FROM yahmlevi/opencv:base
# FROM jjanzic/docker-python3-opencv

# FROM yahmlevi/robo-car:base
FROM eu.gcr.io/video-python/base:latest
WORKDIR /app

COPY /src /app

# troubleshooting: "libdc1394 error: Failed to initialize libdc1394"
# https://hub.docker.com/r/ekazakov/python-opencv
# https://stackoverflow.com/questions/29274638/opencv-libdc1394-error-failed-to-initialize-libdc1394

# ENTRYPOINT ln -s /dev/null /dev/raw1394 && /bin/bash

COPY ./ci/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]