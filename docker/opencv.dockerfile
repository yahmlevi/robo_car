FROM schickling/opencv:latest
WORKDIR /source

# copy the contents of local `source` directory to the image `source` directory
COPY /source /source

CMD ["bash"]
