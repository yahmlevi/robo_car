#! /bin/bash

VERSION=$1

IMAGE="yahmlevi/opencv"
docker run --rm -it --privileged --device=//dev/video0:/dev/video0  $IMAGE:$VERSION