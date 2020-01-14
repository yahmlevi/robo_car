FROM yahmlevi/robo-car:edge-tpu-base
WORKDIR /app

RUN apt update && apt install -y git

RUN git clone https://github.com/google-coral/tflite.git && \
    cd tflite/python/examples/classification && \
    bash install_requirements.sh

COPY edge-tpu-tests.sh /app/tflite/python/examples/classification/edge-tpu-tests.sh 