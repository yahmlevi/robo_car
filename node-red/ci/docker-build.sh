# in CircleCI use /bin/sh (/bin/bash returned 'not found')
#!/bin/sh
set -e

source ../ci/scripts/docker-login.sh

TAG=$1
IMAGE_NAME="$REGISTRY/node-red"
DOCKERFILE="./ci/node-red.dockerfile"

echo "IMAGE_NAME: $IMAGE_NAME"
echo "TAG: $TAG"
echo "DOCKERFILE: $DOCKERFILE"

# build docker image
docker build -t $IMAGE_NAME:$TAG -f $DOCKERFILE .

# tag with "latest"
# docker tag $IMAGE_NAME:$TAG $IMAGE_NAME:latest

# push to DockerHub (both with build number and latest)
docker push $IMAGE_NAME:$TAG
# docker push $IMAGE_NAME:latest
