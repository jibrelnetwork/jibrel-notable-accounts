FROM python:3.7-alpine

ARG ENVIRONMENT="production"

ENV ENVIRONMENT=${ENVIRONMENT} \
    DOCKERIZE_VERSION="v0.6.1"

RUN addgroup -S -g 1000 app \
 && adduser -S -u 1000 -G app -s /bin/sh -D app \
 && mkdir /app \
 && chmod -R ugo=rX /app

WORKDIR /app

COPY --chown=app:app ./requirements /app/requirements/

RUN apk add --no-cache libxml2 libxslt \
 && apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                libxml2-dev \
                libxslt-dev \
                wget \
                openssl \
 && wget --retry-connrefused https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
 && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
 && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN pip install --no-cache-dir -r requirements/base.txt $(test "$ENVIRONMENT" == "development" && echo "-r requirements/base.txt") \
 && apk --purge del .build-deps \
 && rm -rf /var/cache/apk/*

COPY --chown=app:app . /app/
RUN pip install --no-cache-dir /app/

USER app
ENTRYPOINT ["/app/run.sh"]
