#!/bin/bash
set -e

command=$1
IMAGE_TAG=$2

# source - https://docs.docker.com/network/network-tutorial-standalone/
NETWORK_NAME="yahm"

function up(){
    if [[ -z "${IMAGE_TAG}" ]]; then
        echo "Image tag is missing"
        exit 0
    fi

    exists=$(docker network ls | grep -qwz $NETWORK_NAME && echo 'true' || echo 'false')
    if [[ "${exists}" == 'false' ]]; then
        docker network create --driver bridge $NETWORK_NAME
    fi
    docker network inspect $NETWORK_NAME
    docker network ls 
    
    IMAGE_NAME="yahmlevi/python:$IMAGE_TAG"

    docker run -it -d --name "server" --network $NETWORK_NAME $IMAGE_NAME
    docker run -it -d --name "client" --network $NETWORK_NAME $IMAGE_NAME 

    docker container ls
}

# docker network connect bridge "server" 

# Attach (="connect", "get into") to container (each command should be executed in a separate terminal)
function attach_server(){
    docker container attach "server"  
}
function attach_client(){
    docker container attach "client"  
}

function server_up_and_port_forward(){
     docker run -it --rm \
        -v /`pwd`/server.py:/zero-mq/server.py \
        -w //zero-mq \
        -p 5555:5555 \
        yahmlevi/python:buildx bash
}

# Clean up
function down(){
    echo "Stopping containers ..."
    docker container stop "server" "client"

    echo "Removing containers ..."
    docker container rm "server" "client"

    echo "Removing network '$NETWORK_NAME'"
    docker network rm $NETWORK_NAME
}

case $command in
    "up")
        up;;
    "down")
        down;;
    "server")
        attach_server;;
    "client")
        attach_client
esac