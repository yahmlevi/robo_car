#!/bin/bach
set -e

echo "TSADOK"

IMAGE_NAME=$1
TAG=$2
DOCKERFILE=$3

# build docker image
docker build -t $IMAGE_NAME:$TAG -f $DOCKERFILE .

# tag with "latest"
docker tag $IMAGE_NAME:$TAG $IMAGE_NAME:latest

# login to DockerHub
echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

# push to DockerHub (both with build number and latest)
docker push $IMAGE_NAME:$TAG
docker push $IMAGE_NAME:latest