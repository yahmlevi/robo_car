#!/bin/bash
#source - https://docs.docker.com/network/network-tutorial-standalone/
NETWORK_NAME='yahm'

docker network create --driver bridge $NETWORK_NAME
docker network inspect $NETWORK_NAME
#docker network ls 

IMAGE_NAME='yahmlevi/python:43'
docker run -dit --name "server" --network $NETWORK_NAME $IMAGE_NAME
docker run -dit --name "client" --network $NETWORK_NAME $IMAGE_NAME 
docker container ls

# docker network connect bridge "server" 

# Attach (="connect", "get into") to container (each command should be executed in a separate terminal)
# ---------------------------------------
# docker container attach "server"
# docker container attach "client"

# Clean up
# ---------------------------------------
# docker container stop "server" "client"
# docker container rm "server" "client"

# docker network rm $NETWORK_NAME