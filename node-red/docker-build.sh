#!/bin/bash

IMAGE_NAME="yahmlevi/robo-car:node-red"
docker build -t $IMAGE_NAME -f ../docker/dockerfiles/node-red.dockerfile .
docker push $IMAGE_NAME
