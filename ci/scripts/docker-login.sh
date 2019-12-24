#!/bin/sh
set -e

# export DOCKER_USER="yahmlevi"
# export DOCKER_PASS="211367909"


# login to DockerHub
function login_dockerhub() {
    # DOCKER_USER="yahmlevi"
    # DOCKER_PASS="211367909"

    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
}

function login_gcr(){
    export REGISTRY="eu.gcr.io/video-python"
    gcloud auth configure-docker
}



login_gcr


