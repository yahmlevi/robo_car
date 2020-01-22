#!/bin/bash
set -e

command=$1
SUFFIX=$2

if [ -z "$SUFFIX" ]; then
    echo "Invalid suffix for image tag"
    exit 0
fi

case $command in
    "base" )
        source ../../docker/docker-build.sh "build-x" "robo-car" "edge-tpu-base" "edge-tpu-base.dockerfile"
        ;;
    "tests" )
        source ../../docker/docker-build.sh "build-x" "robo-car" "edge-tpu-tests-$SUFFIX" "edge-tpu-tests.dockerfile"
        ;;
    "demo-app" )
        source ../../docker/docker-build.sh "build-x" "robo-car" "edge-tpu-demo-app-$SUFFIX" "edge-tpu-demo-app.dockerfile"
        ;;

    * )
    echo "Invalid command. Please specify 'base', 'tests' or 'demo-app'."
esac