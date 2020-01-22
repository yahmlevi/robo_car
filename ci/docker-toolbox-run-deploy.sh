#! /bin/bash
set -e

IMAGE="yahmlevi/devops-tools:latest"
DOCKERFILE="./devops-tools/devops-tools.dockerfile"

echo "Building DevOps-Tools Docker image"
echo "-------------------------------------------"
docker build -t $IMAGE -f $DOCKERFILE .

echo ""
echo "Running DevOps-Tools container"
echo "-------------------------------------------"
docker run -it --rm \
    -w /k8s \
    -v `pwd`/k8s:/k8s \
    $IMAGE
    
