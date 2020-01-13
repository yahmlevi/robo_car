
#!/bin/bash


command=$1

IMAGE_NAME="tsadok/jenkins"

function docker_build() {
    docker build -t $IMAGE_NAME .
}

function docker_run() {
    
    docker run -d -v //var/run/docker.sock:/var/run/docker.sock \
                -v /"$(which docker):/usr/bin/docker" \
                -p 8080:8080 \
                $IMAGE_NAME
}




case $command in
    "build" )
        docker_build
        ;;
    "run" )
        docker_run
        ;;
esac

