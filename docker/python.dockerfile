FROM python:3.8

COPY test.py test.py
RUN ls -l

CMD ["bash"]
# CMD ["python", "test.py"]
