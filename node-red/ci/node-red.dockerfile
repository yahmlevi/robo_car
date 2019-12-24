FROM nodered/node-red

RUN npm install \
    node-red-contrib-google-cloud \
    node-red-dashboard \
    node-red-contrib-azure-service-bus-queue \
    node-red-contrib-pythonshell \
    node-red-contrib-multipart-stream-decoder \
    node-red-contrib-ffmpeg \
    node-red-node-base64

COPY ./src/data /data
RUN ls -l