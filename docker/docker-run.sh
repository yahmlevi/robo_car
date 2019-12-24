#! /bin/bash

TAG=$1

IMAGE="yahmlevi/opencv"
# docker run --rm -it --privileged --device=//dev/video0:/dev/video0  $IMAGE:$VERSION
# docker run --rm -it --privileged --device=/dev/video0:/dev/video0  $IMAGE:$VERSION

# 1st option
# docker run --rm -it --privileged --device=/dev/video0  $IMAGE:$VERSION

# 2nd option
# https://hub.docker.com/r/sgtwilko/rpi-raspbian-opencv/
# execute 'xhost +' to allow access from the docker container to the host's display
function ols(){
docker run -it --rm \
    -v `pwd`/videos:/videos \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    --device /dev/video0 \
    $IMAGE:$TAG
}

# -v //dev/bus/usb:/dev/bus/usb
# -v //dev/bus/usb:/dev/bus/usb
# //dev/video0:/dev/video0

# -v //dev/video0:/dev/video0
# VIDEOIO ERROR: V4L: device /dev/video0: Unable to query number of channels

# Run GUI app in linux docker container on windows host
# https://dev.to/darksmile92/run-gui-app-in-linux-docker-container-on-windows-host-4kde


function run_video_streamer_client(){
    IMAGE="yahmlevi/robo-car"
    TAG="video-streamer-client"
    
    docker run -it --rm \
        --device /dev/video0 \
        $IMAGE:$TAG
}

REGISTRY="video-python"
function run_video_streamer_server(){
    IMAGE="eu.gcr.io/$REGISTRY/video-streamer-server"
    TAG="latest"
    
    docker run -it --rm \
        -p 5555:5555 \
        -p 8001:8000 \
        --name video-streamer-server \
        $IMAGE:$TAG

    echo "Run the Video Streamer Client on RPI and then goto http://localhost:8001 to see the video stream"    
}