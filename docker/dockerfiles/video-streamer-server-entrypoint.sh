#!/bin/sh 
set -e

HOST_IP=$(ifconfig | grep inet | head -1 | awk '{print $2}') 

echo "HOST_IP: $HOST_IP"

python server.py \
    --prototxt MobileNetSSD_deploy.prototxt \
    --model MobileNetSSD_deploy.caffemodel \
    --montageW 1 \
    --montageH 1 \
    --ip $HOST_IP \
    --port 8000