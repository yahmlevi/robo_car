#!/bin/sh
set -e

export REGISTRY="eu.gcr.io/video-python"

export DOCKER_USER="yahmlevi"
export DOCKER_PASS="211367909"

# login to DockerHub
function login_dockerhub() {
    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
}

# login to gcr
function login_gcr(){
    gcloud auth login   
    gcloud auth configure-docker
}



