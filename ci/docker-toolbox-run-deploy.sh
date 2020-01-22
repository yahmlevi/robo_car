#! /bin/bash

IMAGE="yahmlevi/devops-tools:latest"
DOCKERFILE="./devops-tools/devops-tools.dockerfile"

docker build -t $IMAGE -f $DOCKERFILE .

docker run -it --rm \
    -w /k8s \
    -v `pwd`/k8s:/k8s \
    $IMAGE
    
