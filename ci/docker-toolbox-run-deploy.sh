#! /bin/bash

IMAGE="yahmlevi/devops-tools:latest"

docker build .......

docker run -it --rm \
    -w /k8s \
    -v `pwd`/k8s:/k8s \
    $IMAGE
    
