FROM schickling/opencv:latest
WORKDIR /source

# copy the contents of local `source` directory to the image `source` directory
COPY /source /source


# troubleshooting: "libdc1394 error: Failed to initialize libdc1394"
# https://hub.docker.com/r/ekazakov/python-opencv
# https://stackoverflow.com/questions/29274638/opencv-libdc1394-error-failed-to-initialize-libdc1394
#
# CMD sh -c 'ln -s /dev/null /dev/raw1394'; npm start
 
# CMD ["sh", "-c", "ln -s /dev/null /dev/raw1394", "bash"]
ENTRYPOINT ln -s /dev/null /dev/raw1394 && /bin/bash

