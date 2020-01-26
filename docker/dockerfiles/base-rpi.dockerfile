# FROM schickling/opencv:latest
FROM python:latest
WORKDIR /source

RUN apt-get update && \
    apt-get install -y nano

RUN pip install --upgrade pip zmq imutils
 
# ------------------------------------------------------------

RUN apt update
RUN apt install curl gnupg ca-certificates zlib1g-dev libjpeg-dev -y

# https://stackoverflow.com/questions/24611640/curl-60-ssl-certificate-unable-to-get-local-issuer-certificate/40824910
RUN update-ca-certificates -f

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN apt update
RUN apt install libedgetpu1-std python3 python3-pip python3-edgetpu  -y

# ------------------------------------------------------------

# troubleshooting: "libdc1394 error: Failed to initialize libdc1394"
# https://hub.docker.com/r/ekazakov/python-opencv
# https://stackoverflow.com/questions/29274638/opencv-libdc1394-error-failed-to-initialize-libdc1394

ENTRYPOINT ln -s /dev/null /dev/raw1394 && /bin/bash
