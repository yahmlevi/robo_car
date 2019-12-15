#! /bin/bash

VERSION=$1

IMAGE="yahmlevi/opencv"
docker run --rm -it --privileged --device=//dev/video0:/dev/video0  $IMAGE:$VERSION

# -v //dev/bus/usb:/dev/bus/usb
-v //dev/bus/usb:/dev/bus/usb
//dev/video0:/dev/video0

# -v //dev/video0:/dev/video0
# VIDEOIO ERROR: V4L: device /dev/video0: Unable to query number of channels

# Run GUI app in linux docker container on windows host
# https://dev.to/darksmile92/run-gui-app-in-linux-docker-container-on-windows-host-4kde