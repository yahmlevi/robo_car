#! /bin/bash 
set -e

command=$1

DOCKER_USER="yahmlevi"
DOCKER_PASS="211367909"

IMAGE_NAME=$2
TAG=$3
DOCKERFILE=$4

if [ $# -eq 0 ]; then
    echo "No arguments supplied"
    exit 0
fi

IMAGE_NAME="yahmlevi/$IMAGE_NAME"
# if [[ $IMAGE_NAME == *"-base"* ]]; then
#     IMAGE_NAME="${IMAGE_NAME//-base/}"
#     TAG="base"
# fi

if [[ $DOCKERFILE != *".dockerfile"* ]]; then
    DOCKERFILE="./docker/dockerfiles/$DOCKERFILE.dockerfile"
fi

echo "----------------------------------------------"
echo "IMAGE_NAME=$IMAGE_NAME"
echo "TAG=$TAG"
echo "DOCKERFILE=$DOCKERFILE"
echo "----------------------------------------------"

function docker_login(){
    echo "Login to $DOCKER_USER"
    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
}

function docker_build(){
    # build docker image
    docker build -t $IMAGE_NAME:$TAG -f $DOCKERFILE .

    # tag with "latest"
    # docker tag $IMAGE_NAME:$TAG $IMAGE_NAME:latest

    # login to DockerHub
    docker_login

    # push to DockerHub (both with build number and latest)
    docker push $IMAGE_NAME:$TAG
    # docker push $IMAGE_NAME:latest
}

function docker_build_x(){
    echo "Build docker image using docker-buildx"
    echo ""
    
    # PLATFORMS="linux/amd64,linux/arm64,linux/arm/v7"
    # PLATFORMS="linux/amd64,linux/arm64"
    # PLATFORMS="linux/amd64,linux/arm/v7"
    PLATFORMS="linux/arm/v7"

    echo "First we make sure that we have a suitable builder"
    echo ""
    BUILDER_NAME="multibuilder"
    
    exists=$(docker buildx ls | grep -qZw $BUILDER_NAME && echo 'true' || echo 'false')
    if [[ "${exists}" == 'false' ]]; then
        echo "Creating builder"
        docker buildx create --name $BUILDER_NAME
    fi
    docker buildx inspect $BUILDER_NAME --bootstrap
    docker buildx use $BUILDER_NAME

    # login to DockerHub
    docker_login

    echo "Now we can build using the builder '$BUILDER_NAME'"
    echo ""
    docker buildx build --platform $PLATFORMS -t $IMAGE_NAME:$TAG -f $DOCKERFILE --push .

    echo ""
    docker buildx imagetools inspect $IMAGE_NAME
}

case $command in 
    "build" )
        docker_build
        ;;
    "build-x" )
        docker_build_x
        ;;
    * )
        echo "Please specify a command - 'build' or 'build-x'"
esac
