# FROM schickling/opencv:latest
# FROM mohaseeb/raspberrypi3-python-opencv
# FROM yahmlevi/opencv:base
# FROM jjanzic/docker-python3-opencv

FROM yahmlevi/robo-car:base
WORKDIR /app

# RUN apt-get install software-properties-common && \
#     add-apt-repository ppa:deadsnakes/ppa && \
#     apt-get update && \
#     apt-get install python3.6

# RUN pip install Flask

COPY /video-streamer-server /app

# troubleshooting: "libdc1394 error: Failed to initialize libdc1394"
# https://hub.docker.com/r/ekazakov/python-opencv
# https://stackoverflow.com/questions/29274638/opencv-libdc1394-error-failed-to-initialize-libdc1394

# ENTRYPOINT ln -s /dev/null /dev/raw1394 && /bin/bash
# ENTRYPOINT /bin/bash

# CMD ["python", "server.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel --montageW 1 --montageH 1 --ip 0.0.0.0 --port 8000"]

COPY ./docker/dockerfiles/video-streamer-server-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]

