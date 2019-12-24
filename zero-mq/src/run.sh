#!/bin/bash

command=$1

NETWORK="zero-mq"

function up(){
    # run in 'detach' mode (up -d)
    docker-compose -f docker-compose.yaml up -d 
}
function down(){
    docker-compose -f docker-compose.yaml down 
}
function exec_server(){
    docker exec -it $NETWORK"_server_1" bash
}
function exec_client(){
    docker exec -it $NETWORK"_client_1" bash
}

case $command in 
    "up")
        up;;
    "down")
        down;;
    "server")
        exec_server;;
    "client")
        exec_client;;
esac


    
    