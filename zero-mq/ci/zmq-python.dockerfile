FROM python:3.8

RUN pip install pyzmq
COPY ./src app

WORKDIR /app
CMD ["bash"]
# CMD ["python", "test.py"]
