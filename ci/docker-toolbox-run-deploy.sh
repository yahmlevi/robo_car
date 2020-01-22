#! /bin/bash

IMAGE="google/cloud-sdk:latest"

docker run -it --rm \
    -w /k8s \
    -v `pwd`/k8s:/k8s \
    $IMAGE
    
