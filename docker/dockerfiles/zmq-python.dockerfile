FROM python:3.8

RUN pip install pyzmq
COPY zero-mq zero-mq

WORKDIR /zero-mq
CMD ["bash"]
# CMD ["python", "test.py"]
