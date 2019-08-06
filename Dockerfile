FROM python:3.7-alpine

ARG ENVIRONMENT="production"

ENV API_PORT_PARSER="8080" \
    DB_DSN="" \
    DOCKERIZE_VERSION="v0.6.1" \
    ENVIRONMENT=${ENVIRONMENT} \
    LOG_LEVEL="INFO" \
    NO_JSON_FORMATTER="0" \
    NOTABLE_ACCOUNTS_PARSE_ONCE_DELAY="300" \
    PROXY_PASS="" \
    PROXY_USER="" \
    RAVEN_DSN="" \
    REQUESTS_MAX_WORKERS="10" \
    UPDATE_IF_EXISTS="1"

RUN addgroup -S -g 1000 app \
 && adduser -S -u 1000 -G app -s /bin/sh -D app \
 && mkdir /app \
 && chmod -R ugo=rX /app

WORKDIR /app

COPY --chown=app:app ./requirements /app/requirements/

RUN apk add --no-cache libxml2 libxslt postgresql-libs \
 && apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                libxml2-dev \
                libxslt-dev \
                musl-dev \
                openssl \
                postgresql-dev \
                python3-dev \
                wget \
 && wget --retry-connrefused https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
 && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
 && pip install --no-cache-dir -r requirements/base.txt $(test "$ENVIRONMENT" == "development" && echo "-r requirements/dev.txt") \
 && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
 && apk --purge del .build-deps \
 && rm -rf /var/cache/apk/*

COPY --chown=app:app . /app/
RUN pip install --no-cache-dir /app/

USER app
ENTRYPOINT ["/app/run.sh"]
