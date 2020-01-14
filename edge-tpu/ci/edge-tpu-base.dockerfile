FROM debian:buster

RUN apt update
RUN apt install curl gnupg ca-certificates zlib1g-dev libjpeg-dev -y

# https://stackoverflow.com/questions/24611640/curl-60-ssl-certificate-unable-to-get-local-issuer-certificate/40824910
RUN update-ca-certificates -f

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

RUN apt update
RUN apt install libedgetpu1-std python3 python3-pip python3-edgetpu  -y

RUN curl https://dl.google.com/coral/python/tflite_runtime-1.14.0-cp37-cp37m-linux_armv7l.whl > tflite_runtime-1.14.0-cp37-cp37m-linux_armv7l.whl
RUN pip3 install tflite_runtime-1.14.0-cp37-cp37m-linux_armv7l.whl

# EXPOSE 5005

# ENTRYPOINT ["python3"]
# CMD ["mirror.py"]