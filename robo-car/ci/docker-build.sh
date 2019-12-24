# in CircleCI use /bin/sh (/bin/bash returned 'not found')
#!/bin/sh
set -e

# docker run -it --rm yahmlevi/rob-car:robo-car

source ../ci/scripts/docker-credentials.sh

TAG=$1
IMAGE_NAME=" yahmlevi/robo-car"
DOCKERFILE="./ci/robo-car.dockerfile"

echo "IMAGE_NAME: $IMAGE_NAME"
echo "TAG: $TAG"
echo "DOCKERFILE: $DOCKERFILE"

# build docker image
docker build -t $IMAGE_NAME:$TAG -f $DOCKERFILE .

# tag with "latest"
# docker tag $IMAGE_NAME:$TAG $IMAGE_NAME:latest

# login to DockerHub
echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

# push to DockerHub (both with build number and latest)
docker push $IMAGE_NAME:$TAG
# docker push $IMAGE_NAME:latest
