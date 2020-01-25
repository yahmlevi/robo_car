FROM yahmlevi/robo-car:edge-tpu-base

RUN apt update && apt install -y python3-opencv nano

COPY ./edge-tpu-requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt

COPY ./object_detection /app
WORKDIR /app


# EXPOSE 5005

# ENTRYPOINT ["python3"]
# CMD ["mirror.py"]