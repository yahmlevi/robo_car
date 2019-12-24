FROM yahmlevi/robo-car:base
WORKDIR /app

COPY src /app

COPY ./ci/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]

