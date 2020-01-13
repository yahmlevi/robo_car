FROM yahmlevi/robo-car:edge-tpu-1

RUN apt update && apt install git-all

RUN git clone https://github.com/google-coral/tflite.git && \
    cd tflite/python/examples/classification && \
    bash install_requirements.sh

COPY ./docker/dockerfiles/edge-tpu-tests.sh edge-tpu-tests.sh 