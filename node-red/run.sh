#!/bin/bash

# IMAGE_NAME="nodered/node-red"
IMAGE_NAME="tsadoklf/node-red"

CONTAINER_NAME="mynodered"
DATA_DIR="flows"

# https://github.com/qoomon/docker-host
# https://stackoverflow.com/questions/24319662/from-inside-of-a-docker-container-how-do-i-connect-to-the-localhost-of-the-mach
# --network="host" 

docker run -it --rm -p 1880:1880 --name $CONTAINER_NAME \
    -v /`pwd`/$DATA_DIR:/data \
    $IMAGE_NAME

# docker run -it --rm -p 1880:1880 --name $CONTAINER_NAME \
#     $IMAGE_NAME