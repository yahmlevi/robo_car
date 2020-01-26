# in CircleCI use /bin/sh (/bin/bash returned 'not found')
#!/bin/sh
set -e

source ../../ci/scripts/docker-login.sh

# If DockerHub registry is used
# IMAGE_NAME="yahmlevi/robo-car:node-red"

# If GCR is used
# TAG=$1
# IMAGE_NAME="$REGISTRY/node-red"
# 

TAG="latest"
IMAGE_NAME="$REGISTRY/node-red"
DOCKERFILE="./ci/node-red.dockerfile"

echo "IMAGE_NAME: $IMAGE_NAME"
echo "TAG: $TAG"
echo "DOCKERFILE: $DOCKERFILE"

docker build -t $IMAGE_NAME:$TAG -f $DOCKERFILE .
docker push $IMAGE_NAME:$TAG

