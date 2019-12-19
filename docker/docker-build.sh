#! /bin/bash 
set -e

DOCKER_PASS=211367909
DOCKER_USER=yahmlevi

TAG=$1
IMAGE_NAME="yahmlevi/opencv"
DOCKERFILE="./docker/opencv.dockerfile"

# build docker image
docker build -t $IMAGE_NAME:$TAG -f $DOCKERFILE .

# tag with "latest"
docker tag $IMAGE_NAME:$TAG $IMAGE_NAME:latest

# login to DockerHub
echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

# push to DockerHub (both with build number and latest)
docker push $IMAGE_NAME:$TAG
docker push $IMAGE_NAME:latest
