#! /bin/bash

TAG=$1
IMAGE="google/cloud-sdk"

docker run -it --rm \
    -v ${pwd}/k8s:/k8s \
    $IMAGE:$TAG
    # --volume //c/Users/projects/video-analysis/ci/k8s: /k8s \
    # $IMAGE:$TAG
    
    
